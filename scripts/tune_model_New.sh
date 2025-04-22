#!/bin/bash
# tune_model.sh
# Versão: 1.0.5
# Responsabilidade: Tuning de modelos com LoRA no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

# Verificar se virtualenv está ativado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Verificar se dataset foi fornecido
if [ -z "$1" ]; then
    echo "Error: Please provide a dataset path (e.g., ./dataset.json)."
    exit 1
fi

DATASET_PATH="$1"
MODEL_NAME="${2:-llama_local}"
EPOCHS="${3:-1}"

# Executar tuning com LoRA
echo "Starting model tuning for ${MODEL_NAME} with dataset ${DATASET_PATH}..."
python -m src.backends.tuning.lora_tuning \
    --dataset "$DATASET_PATH" \
    --model "$MODEL_NAME" \
    --epochs "$EPOCHS"

echo "Model tuning completed successfully."