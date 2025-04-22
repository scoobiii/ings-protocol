```python
# qwen_api.py
# Versão: 1.0.5
# Responsabilidade: Backend online para interações com a API Qwen da Alibaba
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import requests
from typing import Dict, Any, List
from src.utils.api_key import get_qwen_api_key

class QwenApiBackend:
    def __init__(self, api_url: str = "https://api.qwen.ai/v1"):
        """Inicializa o backend Qwen com a URL da API."""
        self.api_url = api_url
        self.api_key = get_qwen_api_key()

    async def process_message(self, persona_id: str, message: str, context: List[Dict[str, Any]], mode: str) -> str:
        """Processa uma mensagem usando a API Qwen."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "qwen-turbo",
            "messages": context + [{"role": "user", "content": message}],
            "mode": mode
        }

        response = requests.post(f"{self.api_url}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

# Nota sobre Bend:
# Em Bend, chamadas à API Qwen seriam paralelizadas para múltiplas personas.
# Exemplo: `map(call_qwen_api, messages)`.
# Integração com HTTP exigiria uma biblioteca externa ou binding.
```