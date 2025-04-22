# model_management.py
# Versão: 1.0.5
# Responsabilidade: Endpoint para gerenciar modelos e backends do INGS Protocol
# Data: 2025-04-22
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ModelInfo(BaseModel):
    name: str
    backend_type: str
    status: str

@router.get("/", response_model=List[ModelInfo])
async def list_models(app=Depends(lambda: router.app)):
    async with app.state.postgres_pool.acquire() as conn:
        models = await conn.fetch(
            "SELECT name, model_backend AS backend_type, 'active' AS status FROM personas"
        )
    return [ModelInfo(**model) for model in models]

@router.post("/{model_id}/configure")
async def configure_model(model_id: str, app=Depends(lambda: router.app)):
    # Placeholder para configuração de modelo (ex.: mudar backend)
    return {"status": "success", "message": f"Model {model_id} configured"}

# Nota sobre Bend:
# Listagem de modelos seria uma função pura que consulta o estado do sistema.
# Configuração exigiria integração com bancos de dados via bindings.