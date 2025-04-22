# identity.py
# Versão: 1.0.5
# Responsabilidade: Modelos Pydantic para identidades (DID, API Key) do INGS Protocol
# Data: 2025-04-22
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from pydantic import BaseModel

class DID(BaseModel):
    id: str

class APIKey(BaseModel):
    key: str

# Nota sobre Bend:
# Modelos Pydantic seriam substituídos por tipos algébricos.
# Exemplo: `data DID = DID(String)`