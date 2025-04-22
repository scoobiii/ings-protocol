```python
# interaction.py
# Versão: 1.0.5
# Responsabilidade: Modelos Pydantic para interações no INGS Protocol
# Data: 2025-04-22
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from pydantic import BaseModel
from typing import Dict, Any

class InteractionInput(BaseModel):
    text: str

class InteractionContext(BaseModel):
    persona_id: str
    session_id: str | None = None

class InteractionRequest(BaseModel):
    mode: str
    input_data: InteractionInput
    context: InteractionContext

class InteractionResponse(BaseModel):
    status: str
    response: Dict[str, Any]

# Nota sobre Bend:
# Interações seriam tipos algébricos com pattern-matching.
# Exemplo: `data InteractionRequest = InteractionRequest { mode: String, input: InputData, context: Context }`
```