# runtime.py
# Versão: 1.0.5
# Responsabilidade: Gerenciamento de execução de modelos online e offline no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import logging
from typing import Dict, Any, Optional
from src.backends.offline.llama_local import LlamaLocalBackend
from src.backends.online.xai_grok import XaiGrokBackend
from src.utils.api_key import get_xai_api_key

class RuntimeIntegration:
    def __init__(self):
        """Inicializa o gerenciador de runtime."""
        self.logger = logging.getLogger(__name__)
        self.backends = {
            "llama_local": LlamaLocalBackend(),
            "xai_grok": XaiGrokBackend(api_key=get_xai_api_key())
        }

    async def execute_model(self, model_name: str, persona_id: str, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executa um modelo com base no nome fornecido."""
        if model_name not in self.backends:
            self.logger.error(f"Model {model_name} not supported")
            raise ValueError(f"Model {model_name} not supported")

        backend = self.backends[model_name]
        try:
            response = await backend.process_message(
                persona_id=persona_id,
                message=message,
                context=context or [],
                mode="pragmatic"
            )
            self.logger.info(f"Model {model_name} executed for persona {persona_id}")
            return {"response": response, "model": model_name}
        except Exception as e:
            self.logger.error(f"Failed to execute model {model_name}: {str(e)}")
            raise