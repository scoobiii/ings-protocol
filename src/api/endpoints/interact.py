```python
# interact.py
# Versão: 1.0.5
# Responsabilidade: Endpoint para processar interações 1x1, 1xN, Nx1 com personas INGS
# Data: 2025-04-22
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from fastapi import APIRouter, Depends, HTTPException
from src.api.models.interaction import InteractionRequest, InteractionResponse
from src.backends.online.xai_grok import XaiGrokBackend
from src.backends.offline.llama_local import LlamaLocalBackend
from typing import Dict
import uuid

router = APIRouter()

backends: Dict[str, object] = {
    "xai_grok": XaiGrokBackend(),
    "llama_local": LlamaLocalBackend()
}

@router.post("/", response_model=InteractionResponse)
async def interact(request: InteractionRequest, app=Depends(lambda: router.app)):
    async with app.state.postgres_pool.acquire() as conn:
        persona = await conn.fetchrow(
            "SELECT model_backend FROM personas WHERE persona_id = $1",
            request.context.persona_id
        )
        if not persona:
            raise HTTPException(status_code=404, detail="Persona not found")

    backend = backends.get(persona["model_backend"])
    if not backend:
        raise HTTPException(status_code=400, detail="Backend not supported")

    # Recuperar contexto do ChromaDB
    collection = app.state.chroma.get_collection(f"persona_{request.context.persona_id}")
    context_data = collection.get()

    # Processar interação
    response_data = await backend.process_message(
        persona_id=request.context.persona_id,
        message=request.input_data.text,
        context=context_data,
        mode=request.mode
    )

    # Armazenar interação
    collection.add(
        documents=[request.input_data.text, response_data],
        ids=[str(uuid.uuid4()), str(uuid.uuid4())]
    )

    return InteractionResponse(status="success", response={"text": response_data})

# Nota sobre Bend:
# A interação seria paralelizada para NxN, com uma função que mapeia mensagens
# para múltiplos backends. Exemplo: `map(process_message, personas)`
# Backends offline exigiriam integração com modelos via bindings C/Rust.
```