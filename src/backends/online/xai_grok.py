```python
# xai_grok.py
# Versão: 1.0.5
# Responsabilidade: Backend online para interações com a API Grok da xAI
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import requests
from typing import Dict, Any, List
from src.utils.api_key import get_xai_api_key

class XaiGrokBackend:
    def __init__(self, api_url: str = "https://api.x.ai/grok/v1"):
        """Inicializa o backend Grok com a URL da API."""
        self.api_url = api_url
        self.api_key = get_xai_api_key()

    async def process_message(self, persona_id: str, message: str, context: List[Dict[str, Any]], mode: str) -> str:
        """Processa uma mensagem usando a API Grok."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "grok-3",
            "messages": context + [{"role": "user", "content": message}],
            "mode": mode
        }

        response = requests.post(f"{self.api_url}/chat/completions", json=payload, headers=headers)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

# Nota sobre Bend:
# Chamadas à API Grok seriam paralelizadas em Bend para NxN.
# Exemplo: `def call_grok_api(msg: Message, ctx: List<Context>) -> String`.
# Requer binding HTTP para chamadas externas.
```