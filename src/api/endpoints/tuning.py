# tuning.py
# Versão: 1.0.4
# Responsabilidade: Endpoint para auto-tuning de modelos
# Data: 2025-04-21
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from typing import List, Dict
from src.backends.tuning.lora_tuning import LoRATuner

router = APIRouter()
logger = logging.getLogger(__name__)

class TuningRequest(BaseModel):
    persona_id: str
    training_data: List[Dict]
    lora_config: Dict

@router.post("/tune")
async def tune_model(request: TuningRequest):
    try:
        tuner = LoRATuner(persona_id=request.persona_id, lora_config=request.lora_config)
        tuner.fine_tune(request.training_data)
        logger.info(f"Modelo {request.persona_id} ajustado com sucesso")
        return {"status": "success", "message": "Modelo ajustado"}
    except Exception as e:
        logger.error(f"Erro no tuning: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))