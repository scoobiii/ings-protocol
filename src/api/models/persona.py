```python
# persona.py
# Versão: 1.0.5
# Responsabilidade: Modelos Pydantic para criação e gerenciamento de personas INGS
# Data: 2025-04-22
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from pydantic import BaseModel
from typing import Dict, List

class FileMetadata(BaseModel):
    name: str
    description: str

class CoreParameters(BaseModel):
    capabilities: List[str]
    alignment: str

class BehavioralParameters(BaseModel):
    tone: str
    style: str

class HandshakeRequest(BaseModel):
    schema_version: str
    file_metadata: FileMetadata
    entity_type: str
    core_parameters: CoreParameters
    behavioral_parameters: BehavioralParameters
    model_backend: str

class HandshakeResponse(BaseModel):
    status: str
    persona_id: str
    api_key: str

# Nota sobre Bend:
# Personas seriam tipos algébricos complexos.
# Exemplo: `data HandshakeRequest = HandshakeRequest { schema_version: String, metadata: Metadata, ... }`
```