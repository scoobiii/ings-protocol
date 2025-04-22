```python
# manager.py
# Versão: 1.0.5
# Responsabilidade: Orquestrador NxN para coordenação de sessões multi-agente
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import uuid
import asyncpg
import redis.asyncio as redis
from chromadb import Client as ChromaClient
from src.api.models.session import SessionCreateInput, SessionMessageInput, SessionState
from src.backends.online.xai_grok import XaiGrokBackend
from src.backends.offline.llama_local import LlamaLocalBackend
from src.orchestrator.protocols import InteractionProtocol
from typing import Dict, List, Any

class Orchestrator:
    def __init__(self, postgres_dsn: str, redis_host: str, chromadb_host: str):
        """Inicializa o orquestrador com conexões ao banco e backends."""
        self.postgres_dsn = postgres_dsn
        self.redis = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        self.chroma = ChromaClient(host=chromadb_host, port=8001)
        self.backends: Dict[str, Any] = {
            "xai_grok": XaiGrokBackend(),
            "llama_local": LlamaLocalBackend()
        }
        self.protocol = InteractionProtocol()

    async def create_session(self, request: SessionCreateInput) -> str:
        """Cria uma nova sessão NxN."""
        session_id = str(uuid.uuid4())
        async with asyncpg.create_pool(self.postgres_dsn) as pool:
            async with pool.acquire() as conn:
                await conn.execute(
                    """
                    INSERT INTO sessions (session_id, participants, rules, status)
                    VALUES ($1, $2, $3, $4)
                    """,
                    session_id, request.participants, 
                    request.session_rules.dict() if request.session_rules else {},
                    "active"
                )
        self.chroma.get_or_create_collection(f"session_{session_id}")
        return session_id

    async def send_message(self, session_id: str, request: SessionMessageInput) -> Dict[str, str]:
        """Envia uma mensagem e processa respostas de participantes."""
        async with asyncpg.create_pool(self.postgres_dsn) as pool:
            async with pool.acquire() as conn:
                session = await conn.fetchrow(
                    "SELECT participants, rules FROM sessions WHERE session_id = $1 AND status = $2",
                    session_id, "active"
                )
                if not session:
                    raise ValueError("Session not found or inactive")

        # Recuperar contexto
        collection = self.chroma.get_collection(f"session_{session_id}")
        context = collection.get()

        # Aplicar protocolo de roteamento
        recipients = self.protocol.route_message(
            sender_id=request.sender_id,
            participants=session["participants"],
            rules=session["rules"],
            message=request.message_data
        )

        # Processar respostas em paralelo
        responses = {}
        for recipient_id in recipients:
            persona = await self._get_persona(recipient_id, pool)
            backend = self.backends.get(persona["model_backend"])
            if backend:
                response = await backend.process_message(
                    persona_id=recipient_id,
                    message=request.message_data,
                    context=context,
                    mode=session["rules"].get("mode", "pragmatic")
                )
                responses[recipient_id] = response
                collection.add(
                    documents=[request.message_data, response],
                    ids=[str(uuid.uuid4()), str(uuid.uuid4())]
                )

        return responses

    async def get_session_state(self, session_id: str) -> SessionState:
        """Recupera o estado de uma sessão."""
        async with asyncpg.create_pool(self.postgres_dsn) as pool:
            async with pool.acquire() as conn:
                session = await conn.fetchrow(
                    "SELECT participants, rules, status FROM sessions WHERE session_id = $1",
                    session_id
                )
                if not session:
                    raise ValueError("Session not found")
        
        collection = self.chroma.get_collection(f"session_{session_id}")
        history = collection.get()
        return SessionState(
            session_id=session_id,
            participants=session["participants"],
            rules=session["rules"],
            history=history
        )

    async def terminate_session(self, session_id: str) -> Dict[str, str]:
        """Encerra uma sessão."""
        async with asyncpg.create_pool(self.postgres_dsn) as pool:
            async with pool.acquire() as conn:
                await conn.execute(
                    "UPDATE sessions SET status = $1 WHERE session_id = $2",
                    "terminated", session_id
                )
        return {"status": "terminated"}

    async def _get_persona(self, persona_id: str, pool: asyncpg.Pool) -> Dict[str, Any]:
        """Recupera metadados de uma persona."""
        async with pool.acquire() as conn:
            persona = await conn.fetchrow(
                "SELECT model_backend, crypto_address FROM personas WHERE persona_id = $1",
                persona_id
            )
            if not persona:
                raise ValueError(f"Persona {persona_id} not found")
            return persona

# Nota sobre Bend:
# Em Bend, o Orchestrator seria implementado como uma função funcional que processa mensagens em paralelo.
# Exemplo: `def process_session(session: Session, messages: List<Message>) -> List<Response>`
# O roteamento NxN seria paralelizado massivamente, usando HVM2 para GPUs.
# Integração com PostgreSQL/ChromaDB exigiria bindings C/Rust.
```