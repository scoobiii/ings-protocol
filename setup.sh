#!/bin/bash
# requirements_update.sh
# Versão: 1.0.5
# Responsabilidade: Atualizar dependências do INGS Protocol com versões mais recentes
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

echo "Atualizando dependências do INGS Protocol..."

# Verificar se está em um ambiente virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Ativando ambiente virtual..."
    source .venv/bin/activate
else
    echo "Ambiente virtual ativo: $VIRTUAL_ENV"
fi

# Atualizar pip
echo "Atualizando pip..."
pip install --upgrade pip

# Atualizar dependências
echo "Instalando dependências mais recentes..."
pip install --upgrade -r requirements.txt

# Gerar requirements.txt com versões instaladas
echo "Gerando requirements.txt com versões atuais..."
pip freeze > requirements.txt

# Testar importação de dependências
echo "Testando importação de dependências..."
python3 -c "import fastapi, uvicorn, pydantic, docker, python_dotenv, pytest, asyncpg, redis, requests, transformers, torch, peft, chromadb, sentence_transformers, lmql" || {
    echo "Erro: Falha ao importar dependências. Verifique compatibilidade."
    exit 1
}

echo "Atualização concluída! Verifique requirements.txt para as versões instaladas."