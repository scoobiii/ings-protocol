# validator.py
# Versão: 1.0.5
# Responsabilidade: Validação genérica de dados no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import logging
from typing import Any, Dict
from pydantic import BaseModel, ValidationError

class Validator:
    def __init__(self):
        """Inicializa o validador genérico."""
        self.logger = logging.getLogger(__name__)

    def validate_data(self, data: Dict[str, Any], model: BaseModel) -> bool:
        """Valida dados contra um modelo Pydantic."""
        try:
            model(**data)
            self.logger.info("Data validated successfully")
            return True
        except ValidationError as e:
            self.logger.warning(f"Data validation failed: {str(e)}")
            return False