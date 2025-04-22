# tests/unit/test_handshake.py
# Versão: 1.0.5
# Responsabilidade: Testes unitários para o endpoint /handshake no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.utils.crypto_id import generate_did

client = TestClient(app)

def test_handshake_success():
    """Testa o sucesso do endpoint /handshake."""
    response = client.post("/handshake", json={"persona_name": "test_persona", "model_type": "llm"})
    assert response.status_code == 200
    assert "persona_id" in response.json()
    assert generate_did(response.json()["persona_id"]).startswith("did:nings:artificial:llm")

def test_handshake_invalid_input():
    """Testa o endpoint /handshake com entrada inválida."""
    response = client.post("/handshake", json={"persona_name": ""})
    assert response.status_code == 422  # Unprocessable Entity