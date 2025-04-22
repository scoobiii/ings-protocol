# pragmatic.py
# Versão: 1.0.5
# Responsabilidade: Modo pragmático para respostas diretas e práticas no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import logging
from typing import Dict, Any, List
from src.utils.message_validator import MessageValidator
from src.utils.ethics import EthicsChecker
from src.protocols.json_nl import JsonNLProtocol

class PragmaticMode:
    def __init__(self):
        """Inicializa o modo pragmático."""
        self.logger = logging.getLogger(__name__)
        self.validator = MessageValidator()
        self.ethics_checker = EthicsChecker()
        self.json_protocol = JsonNLProtocol()

    async def process_interaction(self, session_id: str, message: Dict[str, Any], participants: List[str], context: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processa uma interação no modo pragmático."""
        try:
            # Validar mensagem
            if not self.validator.validate_interaction(message):
                self.logger.warning(f"Invalid message in session {session_id}")
                return []
            if not self.ethics_checker.check_message(message["message_data"], context):
                self.logger.warning(f"Message failed ethical checks in session {session_id}")
                return []

            # Codificar mensagem em JSON-NL
            json_message = self.json_protocol.encode_message(message)

            # Gerar resposta direta do primeiro participante
            response = {
                "sender_id": participants[0],
                "message_data": f"Direct response: {message['message_data']}",  # Placeholder
                "timestamp": message["timestamp"],
                "metadata": {"mode": "pragmatic"}
            }
            self.logger.info(f"Generated pragmatic response for {participants[0]} in session {session_id}")

            return [response]
        except Exception as e:
            self.logger.error(f"Failed to process pragmatic interaction: {str(e)}")
            return []