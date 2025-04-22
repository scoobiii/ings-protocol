```python
# session.py
# Versão: 1.0.5
# Responsabilidade: Endpoint para gerenciar sessões NxN multi-agente
# Data: 2025-04-22
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from fastapi import APIRouter, Depends, HTTPException
from src.api.models.session import SessionCreateInput, SessionMessageInput, SessionState
from src.orchestrator.manager import Orchestrator

router = APIRouter()

@router.post("/create")
async def create_session(request: SessionCreateInput, app=Depends(lambda: router.app)):
    orchestrator = Orchestrator(
        postgres_dsn="postgresql://user:password@localhost:5432/ings_db",
        redis_host="localhost",
        chromadb_host="localhost"
    )
    session_id = await orchestrator.create_session(request)
    return {"session_id": session_id}

@router.post("/{session_id}/message")
async def send_message(session_id: str, request: SessionMessageInput, app=Depends(lambda: router.app)):
    orchestrator = Orchestrator(
        postgres_dsn="postgresql://user:password@localhost:5432/ings_db",
        redis_host="localhost",
        chromadb_host="localhost"
    )
    responses = await orchestrator.send_message(session_id, request)
    return responses

@router.get("/{session_id}/state")
async def get_session_state(session_id: str, app=Depends(lambda: router.app)):
    orchestrator = Orchestrator(
        postgres_dsn="postgresql://user:password@localhost:5432/ings_db",
        redis_host="localhost",
        chromadb_host="localhost"
    )
    state = await orchestrator.get_session_state(session_id)
    return state

@router.post("/{session_id}/terminate")
async def terminate_session(session_id: str, app=Depends(lambda: router.app)):
    orchestrator = Orchestrator(
        postgres_dsn="postgresql://user:password@localhost:5432/ings_db",
        redis_host="localhost",
        chromadb_host="localhost"
    )
    result = await orchestrator.terminate_session(session_id)
    return result

# Nota sobre Bend:
# Sessões NxN são ideais para Bend, com paralelismo massivo para roteamento de mensagens.
# Exemplo: `def process_session_messages(session: Session, messages: List<Message>)`
# O Orchestrator seria o principal componente em Bend, with gRPC para integração com Python.
```