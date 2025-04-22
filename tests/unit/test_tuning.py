# tests/unit/test_tuning.py
# Versão: 1.0.5
# Responsabilidade: Testes unitários para tuning de modelos no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import pytest
from src.backends.tuning.lora_tuning import LoRATuner

@pytest.mark.asyncio
async def test_lora_tuning():
    """Testa o tuning com LoRA."""
    tuner = LoRATuner(model_name="llama_local")
    dataset = [{"input": "Hello", "output": "Hi!"}]
    result = await tuner.tune(dataset, epochs=1)
    assert "status" in result
    assert result["status"] == "success"