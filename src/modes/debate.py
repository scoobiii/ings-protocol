# debate.py
# Versão: 1.0.5
# Responsabilidade: Modo de debate para discussões estruturadas no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import logging
from typing import Dict, Any, List
from src.utils.message_validator import MessageValidator
from src.utils.ethics import EthicsChecker
from src.protocols.json_nl import JsonNLProtocol

class DebateMode:
    def __init__(self):
        """Inicializa o modo de debate."""
        self.logger = logging.getLogger(__name__)
        self.validator = MessageValidator()
        self.ethics_checker = EthicsChecker()
        self.json_protocol = JsonNLProtocol()

    async def process_interaction(self, session_id: str, message: Dict[str, Any], participants: List[str], context: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processa uma interação no modo debate."""
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

            # Gerar respostas alternadas (pró e contra)
            responses = []
            for i, participant in enumerate(participants):
                stance = "pro" if i % 2 == 0 else "contra"
                response = {
                    "sender_id": participant,
                    "message_data": f"{stance.capitalize()} argument from {participant}: {message['message_data']}",  # Placeholder
                    "timestamp": message["timestamp"],
                    "metadata": {"mode": "debate", "stance": stance}
                }
                responses.append(response)
                self.logger.info(f"Generated {stance} argument for {participant} in session {session_id}")

            return responses
        except Exception as e:
            self.logger.error(f"Failed to process debate interaction: {str(e)}")
            return []