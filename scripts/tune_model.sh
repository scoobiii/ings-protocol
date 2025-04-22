```bash
#!/bin/bash
# tune_model.sh
# Versão: 1.0.4
# Responsabilidade: Automatizar o auto-tuning de modelos com LoRA
# Data: 2025-04-21
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

echo "Iniciando auto-tuning do modelo INGS..."

# Verificar se o ambiente virtual existe e ativá-lo
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Erro: Ambiente virtual não encontrado. Execute setup.sh primeiro."
    exit 1
fi

# Verificar argumentos
if [ $# -lt 2 ]; then
    echo "Uso: $0 <persona_id> <training_data_json>"
    echo "Exemplo: $0 did:nings:artificial:llm:techlead:v2.0:a7f3b9d2c8e1 data.json"
    exit 1
fi

PERSONA_ID=$1
TRAINING_DATA=$2

# Verificar se o arquivo de dados existe
if [ ! -f "$TRAINING_DATA" ]; then
    echo "Erro: Arquivo $TRAINING_DATA não encontrado."
    exit 1
fi

# Configuração padrão do LoRA
LORA_CONFIG='{"model_name":"meta-llama/Llama-3.1-8B","rank":8,"alpha":16}'

# Enviar solicitação de tuning
echo "Enviando solicitação de tuning para $PERSONA_ID..."
curl -X POST http://localhost:8000/tune \
    -H "Content-Type: application/json" \
    -d "{\"persona_id\":\"$PERSONA_ID\",\"training_data\":$(cat $TRAINING_DATA),\"lora_config\":$LORA_CONFIG}" \
    | tee tuning_result.json

# Verificar se o tuning foi bem-sucedido
if grep -q '"status":"success"' tuning_result.json; then
    echo "Tuning concluído com sucesso!"
else
    echo "Erro no tuning. Verifique tuning_result.json para detalhes."
    exit 1
fi

rm tuning_result.json
echo "Modelo ajustado para $PERSONA_ID."
```