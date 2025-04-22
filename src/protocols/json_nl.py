```python
# json_nl.py
# Versão: 1.0.5
# Responsabilidade: Protocolo JSON para mensagens em linguagem natural no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import json
from typing import Dict, Any, List
from pydantic import BaseModel, ValidationError
from src.utils.message_validator import MessageValidator
from src.utils.ethics import EthicsChecker
import logging

class JsonNLMessage(BaseModel):
    sender_id: str
    message_data: str
    timestamp: str
    context: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}

class JsonNLProtocol:
    def __init__(self):
        """Inicializa o protocolo JSON-NL."""
        self.logger = logging.getLogger(__name__)
        self.validator = MessageValidator()
        self.ethics_checker = EthicsChecker()

    def encode_message(self, message: JsonNLMessage) -> str:
        """Codifica uma mensagem em JSON."""
        try:
            json_str = message.json()
            if not self.validator.validate(json_str, {"require_json": True}):
                self.logger.warning("Invalid JSON-NL message format")
                raise ValueError("Invalid JSON-NL message format")
            if not self.ethics_checker.check_message(message.message_data, message.context):
                self.logger.warning("Message failed ethical checks")
                raise ValueError("Message failed ethical checks")
            self.logger.info("Message encoded successfully")
            return json_str
        except ValidationError as e:
            self.logger.error(f"Failed to encode message: {str(e)}")
            raise

    def decode_message(self, json_str: str) -> JsonNLMessage:
        """Decodifica uma mensagem JSON em objeto."""
        try:
            if not self.validator.validate(json_str, {"require_json": True}):
                self.logger.warning("Invalid JSON-NL message format")
                raise ValueError("Invalid JSON-NL message format")
            message = JsonNLMessage(**json.loads(json_str))
            if not self.ethics_checker.check_message(message.message_data, message.context):
                self.logger.warning("Message failed ethical checks")
                raise ValueError("Message failed ethical checks")
            self.logger.info("Message decoded successfully")
            return message
        except (json.JSONDecodeError, ValidationError) as e:
            self.logger.error(f"Failed to decode message: {str(e)}")
            raise

# Nota sobre Bend:
# O protocolo seria uma função pura para codificação/decodificação.
# Exemplo: `def encode_json_nl(msg: JsonNLMessage) -> String`
# Paralelização seria aplicada para processar milhares de mensagens no Orchestrator NxN.
```