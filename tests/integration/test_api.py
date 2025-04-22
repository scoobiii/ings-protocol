# tests/integration/test_api.py
# Versão: 1.0.5
# Responsabilidade: Testes de integração para a API FastAPI no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import pytest
import httpx
from fastapi.testclient import TestClient
from src.api.main import app
from src.utils.crypto_id import generate_did

@pytest.mark.asyncio
async def test_api_handshake():
    """Testa o endpoint /handshake."""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/handshake", json={"persona_name": "test_persona", "model_type": "llm"})
        assert response.status_code == 200
        assert "persona_id" in response.json()
        assert generate_did(response.json()["persona_id"]).startswith("did:nings:artificial:llm")

@pytest.mark.asyncio
async def test_api_interact():
    """Testa o endpoint /interact."""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        # Primeiro, criar persona via handshake
        handshake_response = await client.post("/handshake", json={"persona_name": "test_persona", "model_type": "llm"})
        persona_id = handshake_response.json()["persona_id"]

        # Testar interação
        interaction_data = {
            "persona_id": persona_id,
            "message": "Hello, world!",
            "mode": "pragmatic"
        }
        response = await client.post("/interact", json=interaction_data)
        assert response.status_code == 200
        assert "response" in response.json()