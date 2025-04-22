# test_full_stack.py
# Versão: 1.0.5
# Responsabilidade: Teste de integração completo para o INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import pytest
import asyncpg
from fastapi.testclient import TestClient
from src.api.main import app
from src.integrations.vector_db import VectorDB
from src.integrations.blockchain import BlockchainClient

client = TestClient(app)

@pytest.mark.asyncio
async def test_full_stack_flow():
    """Testa o fluxo completo: handshake, interação, armazenamento e blockchain."""
    # Configuração do banco
    pool = await asyncpg.create_pool(
        host="localhost", port=5432, database="ings_db",
        user="ings_user", password="secure_password"
    )
    vector_db = VectorDB()
    blockchain = BlockchainClient()

    # Handshake: criar persona
    persona_data = {
        "persona_name": "TestPersona",
        "model_type": "xai_grok"
    }
    response = client.post("/handshake", json=persona_data)
    assert response.status_code == 200
    persona_id = response.json()["persona_id"]

    # Verificar no PostgreSQL
    persona = await pool.fetchrow("SELECT * FROM personas WHERE persona_id = $1", persona_id)
    assert persona["name"] == "TestPersona"

    # Verificar no ChromaDB
    persona_embedding = vector_db.search_personas("TestPersona", limit=1)
    assert persona_embedding[0]["metadata"]["persona_id"] == persona_id

    # Interagir
    interaction_data = {
        "persona_id": persona_id,
        "message": "Test message",
        "mode": "pragmatic"
    }
    response = client.post("/interact", json=interaction_data)
    assert response.status_code == 200
    interaction_response = response.json()["response"]

    # Verificar interação no PostgreSQL
    interaction = await pool.fetchrow("SELECT * FROM interactions WHERE persona_id = $1", persona_id)
    assert interaction["message"] == "Test message"

    # Verificar no ChromaDB
    interaction_embedding = vector_db.search_interactions("Test message", limit=1)
    assert interaction_embedding[0]["metadata"]["persona_id"] == persona_id

    # Verificar no blockchain
    blockchain_interaction = await blockchain.get_interaction(0)
    assert blockchain_interaction["message"] == "Test message"

    await pool.close()