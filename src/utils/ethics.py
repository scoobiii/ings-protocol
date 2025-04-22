```python
# ethics.py
# Versão: 1.0.5
# Responsabilidade: Verificações éticas para mensagens e interações no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from typing import Dict, Any, List
import re
import logging

class EthicsChecker:
    def __init__(self):
        """Inicializa o verificador ético com regras padrão."""
        self.logger = logging.getLogger(__name__)
        self.forbidden_topics = [
            "violence", "hate_speech", "discrimination", "illegal_activities"
        ]
        self.sensitive_patterns = [
            re.compile(r'\b(kill|murder|assault)\b', re.IGNORECASE),
            re.compile(r'\b(race|religion|gender)\b.*\b(hate|attack)\b', re.IGNORECASE)
        ]
        self.max_risk_score = 0.9  # Threshold para rejeição

    def check_message(self, message: str, context: List[Dict[str, Any]], rules: Dict[str, Any] = None) -> bool:
        """Verifica se uma mensagem viola diretrizes éticas."""
        if not message:
            self.logger.warning("Empty message received")
            return False

        # Verificar tópicos proibidos
        for topic in self.forbidden_topics:
            if topic in message.lower():
                self.logger.warning(f"Message contains forbidden topic: {topic}")
                return False

        # Verificar padrões sensíveis
        for pattern in self.sensitive_patterns:
            if pattern.search(message):
                self.logger.warning(f"Message matches sensitive pattern: {pattern.pattern}")
                return False

        # Verificar contexto (ex.: histórico de violações)
        if context:
            risk_score = self._calculate_risk_score(context)
            if risk_score > self.max_risk_score:
                self.logger.warning(f"Message context exceeds risk score: {risk_score}")
                return False

        # Aplicar regras personalizadas
        if rules and "forbidden_words" in rules:
            if any(word.lower() in message.lower() for word in rules["forbidden_words"]):
                self.logger.warning("Message contains forbidden words from rules")
                return False

        self.logger.info("Message passed ethical checks")
        return True

    def _calculate_risk_score(self, context: List[Dict[str, Any]]) -> float:
        """Calcula um score de risco com base no contexto."""
        # Placeholder: Analisar histórico de mensagens
        violation_count = sum(1 for msg in context if "violation" in msg.get("metadata", {}))
        return min(1.0, violation_count / len(context)) if context else 0.0

    def flag_violation(self, message: str, reason: str):
        """Registra uma violação ética."""
        self.logger.error(f"Ethical violation detected: {reason} in message: {message}")
        # Placeholder: Enviar alerta ou registrar no banco
        pass

# Nota sobre Bend:
# Verificações éticas seriam funções puras com pattern-matching.
# Exemplo: `def check_message(msg: String, ctx: List<Context>, rules: Rules) -> Bool`
# Paralelização seria aplicada para validar milhares de mensagens simultaneamente.
```