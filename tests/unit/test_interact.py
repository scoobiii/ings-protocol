# tests/unit/test_interact.py
# Versão: 1.0.5
# Responsabilidade: Testes unitários para o endpoint /interact no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.utils.crypto_id import generate_did

client = TestClient(app)

def test_interact_success():
    """Testa o sucesso do endpoint /interact."""
    # Criar persona via handshake
    handshake_response = client.post("/handshake", json={"persona_name": "test_persona", "model_type": "llm"})
    persona_id = handshake_response.json()["persona_id"]

    # Testar interação
    interaction_data = {
        "persona_id": persona_id,
        "message": "Hello, world!",
        "mode": "pragmatic"
    }
    response = client.post("/interact", json=interaction_data)
    assert response.status_code == 200
    assert "response" in response.json()

def test_interact_invalid_persona():
    """Testa o endpoint /interact com persona inválida."""
    interaction_data = {
        "persona_id": "invalid_persona",
        "message": "Hello, world!",
        "mode": "pragmatic"
    }
    response = client.post("/interact", json=interaction_data)
    assert response.status_code == 404  # Not Found