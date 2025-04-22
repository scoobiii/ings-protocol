```python
# message_validator.py
# Versão: 1.0.5
# Responsabilidade: Validação técnica de mensagens para formato, sintaxe e segurança no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from typing import Dict, Any, Optional
import re
import json
import logging
from pydantic import ValidationError
from src.api.models.interaction import InteractionInput

class MessageValidator:
    def __init__(self):
        """Inicializa o validador de mensagens com regras padrão."""
        self.logger = logging.getLogger(__name__)
        self.max_length = 1000
        self.allowed_chars = re.compile(r'^[a-zA-Z0-9\s.,!?@#$%^&*()_+\-=\[\]{}\\|;:"\'<>?/~`]*$')
        self.json_required_fields = ["sender_id", "message_data"]

    def validate(self, message: str, rules: Dict[str, Any] = None) -> bool:
        """Valida uma mensagem quanto a formato, sintaxe e segurança."""
        rules = rules or {}

        # Verificar comprimento
        max_length = rules.get("max_length", self.max_length)
        if len(message) > max_length:
            self.logger.warning(f"Message exceeds max length: {len(message)} > {max_length}")
            return False

        # Verificar caracteres permitidos
        if not self.allowed_chars.match(message):
            self.logger.warning("Message contains invalid characters")
            return False

        # Verificar estrutura JSON (se aplicável)
        try:
            if rules.get("require_json", False):
                json_data = json.loads(message)
                for field in self.json_required_fields:
                    if field not in json_data:
                        self.logger.warning(f"Missing required JSON field: {field}")
                        return False
        except json.JSONDecodeError:
            self.logger.warning("Invalid JSON format")
            return False

        self.logger.info("Message passed technical validation")
        return True

    def validate_interaction(self, interaction: Dict[str, Any]) -> bool:
        """Valida uma interação usando o modelo Pydantic InteractionInput."""
        try:
            InteractionInput(**interaction)
            self.logger.info("Interaction passed Pydantic validation")
            return True
        except ValidationError as e:
            self.logger.warning(f"Invalid interaction: {str(e)}")
            return False

    def sanitize(self, message: str) -> str:
        """Sanitiza uma mensagem removendo caracteres indesejados."""
        sanitized = re.sub(r'[^\w\s.,!?]', '', message)
        self.logger.info("Message sanitized")
        return sanitized

    def log_invalid_message(self, message: str, reason: str):
        """Registra uma mensagem inválida para auditoria."""
        self.logger.error(f"Invalid message: {reason} | Content: {message}")
        # Placeholder: Registrar no blockchain ou banco para auditoria
        # Exemplo: chamar src/integrations/blockchain.py para log imutável
        pass

# Nota sobre Bend:
# Validação seria uma função pura com pattern-matching.
# Exemplo: `def validate_message(msg: String, rules: Rules) -> Bool`
# Sanitização e validação seriam paralelizáveis para milhares de mensagens no Orchestrator NxN.
```