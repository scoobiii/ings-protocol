# tests/social_turing/test_social_interaction.py
# Versão: 1.0.5
# Responsabilidade: Testes para o modo social Turing no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import pytest
from src.modes.social_turing import SocialTuringMode
from src.utils.crypto_id import generate_did

@pytest.mark.asyncio
async def test_social_turing_interaction():
    """Testa uma interação no modo social Turing."""
    mode = SocialTuringMode()
    session_id = "test_session"
    message = {
        "sender_id": generate_did("test_persona:llm:v2.0"),
        "message_data": "I'm feeling sad today.",
        "timestamp": "2025-04-23T12:00:00Z"
    }
    participants = ["persona_1"]
    context = []

    responses = await mode.process_interaction(session_id, message, participants, context)
    assert len(responses) == 1
    assert responses[0]["sender_id"] == participants[0]
    assert "Empathetic response" in responses[0]["message_data"]