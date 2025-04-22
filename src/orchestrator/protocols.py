```python
# protocols.py
# Versão: 1.0.5
# Responsabilidade: Protocolos de roteamento e regras para interações NxN
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from typing import List, Dict, Any

class InteractionProtocol:
    def route_message(self, sender_id: str, participants: List[str], rules: Dict[str, Any], message: str) -> List[str]:
        """Determina os destinatários de uma mensagem com base nas regras."""
        mode = rules.get("mode", "round-robin")
        if mode == "round-robin":
            # Enviar para o próximo participante na lista
            idx = participants.index(sender_id) if sender_id in participants else -1
            next_idx = (idx + 1) % len(participants)
            return [participants[next_idx]]
        elif mode == "broadcast":
            # Enviar para todos, exceto o remetente
            return [p for p in participants if p != sender_id]
        elif mode == "direct":
            # Extrair menções diretas do texto (ex.: "@persona_id")
            mentions = [p for p in participants if f"@{p}" in message]
            return mentions if mentions else participants[:1]  # Fallback para o primeiro
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def validate_message(self, message: str, rules: Dict[str, Any]) -> bool:
        """Valida uma mensagem com base nas regras da sessão."""
        max_length = rules.get("max_length", 1000)
        return len(message) <= max_length

# Nota sobre Bend:
# Protocolos seriam funções puras com pattern-matching.
# Exemplo: `def route_message(sender: String, participants: List<String>, rules: Rules) -> List<String>`
# O roteamento seria paralelizado para milhares de mensagens.
```