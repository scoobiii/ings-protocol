#!/bin/bash
# validate_deps.sh
# Versão: 1.0.5
# Responsabilidade: Validar dependências instaladas para o INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

echo "Validando dependências do INGS Protocol..."

# Verificar se está em um ambiente virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Ativando ambiente virtual..."
    source .venv/bin/activate
else
    echo "Ambiente virtual ativo: $VIRTUAL_ENV"
fi

# Testar importação de dependências principais
echo "Testando importação de dependências..."
python3 -c "import fastapi, uvicorn, pydantic, docker, python_dotenv, pytest, asyncpg, redis, requests, transformers, torch, peft, chromadb, sentence_transformers, lmql" || {
    echo "Erro: Falha ao importar dependências. Verifique compatibilidade."
    exit 1
}

# Verificar versões instaladas contra requirements.txt
echo "Verificando compatibilidade com requirements.txt..."
pip check || {
    echo "Aviso: Incompatibilidades detectadas. Considere ajustar requirements.txt ou requirements.lock."
}

# Testar inicialização básica da API
echo "Testando inicialização da API..."
python3 -c "from src.api.main import app" || {
    echo "Erro: Falha ao importar a API. Verifique src/api/main.py."
    exit 1
}

# Testar conexão com PostgreSQL
echo "Testando conexão com PostgreSQL..."
python3 -c "
import asyncpg
async def test_db():
    conn = await asyncpg.connect(
        host='localhost', port=5432, database='ings_db',
        user='ings_user', password='secure_password'
    )
    await conn.close()
import asyncio
asyncio.run(test_db())
" || {
    echo "Erro: Falha na conexão com PostgreSQL. Verifique .env e scripts/init_db.sql."
    exit 1
}

# Testar ChromaDB
echo "Testando ChromaDB..."
python3 -c "from chromadb import Client; Client()" || {
    echo "Erro: Falha ao inicializar ChromaDB. Verifique src/integrations/vector_db.py."
    exit 1
}

echo "Validação concluída! Dependências estão compatíveis."
echo "Para iniciar a API, execute:"
echo "source .venv/bin/activate && uvicorn src.api.main:app --host 0.0.0.0 --port 8000"