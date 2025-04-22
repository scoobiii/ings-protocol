# handshake.py
# Versão: 1.0.5
# Responsabilidade: Endpoint para criar e gerenciar personas INGS com IDs criptográficos (DID)
# Data: 2025-04-22
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from fastapi import APIRouter, Depends, HTTPException
from src.api.models.persona import HandshakeRequest, HandshakeResponse
from src.utils.crypto_id import generate_did
from src.utils.api_key import generate_api_key
import asyncpg

router = APIRouter()

@router.post("/", response_model=HandshakeResponse)
async def create_persona(request: HandshakeRequest, app=Depends(lambda: router.app)):
    async with app.state.postgres_pool.acquire() as conn:
        # Validar backend
        valid_backends = ["xai_grok", "qwen_api", "llama_local", "mistral_local"]
        if request.model_backend not in valid_backends:
            raise HTTPException(status_code=400, detail="Invalid model backend")

        # Gerar DID e API Key
        persona_id = generate_did(f"llm:{request.file_metadata.name}:{request.schema_version}")
        api_key = generate_api_key()

        # Persistir persona
        await conn.execute(
            """
            INSERT INTO personas (persona_id, name, model_backend, metadata, api_key)
            VALUES ($1, $2, $3, $4, $5)
            """,
            persona_id, request.file_metadata.name, request.model_backend,
            request.dict(), api_key
        )

        # Inicializar coleção ChromaDB
        app.state.chroma.get_or_create_collection(f"persona_{persona_id}")

        return HandshakeResponse(
            status="success",
            persona_id=persona_id,
            api_key=api_key
        )

# Nota sobre Bend:
# O handshake seria uma função pura que valida inputs e gera DID/API Key.
# Exemplo: `def create_persona(req: HandshakeRequest) -> HandshakeResponse`
# A persistência em PostgreSQL exigiria um binding externo ou reimplementação.