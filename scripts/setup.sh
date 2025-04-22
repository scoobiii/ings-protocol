#!/bin/bash
# setup.sh
# Versão: 1.0.5
# Responsabilidade: Configurar o ambiente para o projeto INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

echo "Configurando o ambiente para o INGS Protocol..."

# Verificar se o Python 3.9+ está instalado
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]; }; then
    echo "Erro: Python 3.9 ou superior é necessário. Versão atual: $PYTHON_VERSION"
    exit 1
fi
echo "Python $PYTHON_VERSION detectado."

# Verificar se está em um ambiente virtual
if [ -z "$VIRTUAL_ENV" ]; then
    # Criar e ativar ambiente virtual
    if [ ! -d ".venv" ]; then
        echo "Criando ambiente virtual..."
        python3 -m venv .venv
    fi
    source .venv/bin/activate
else
    echo "Ambiente virtual já ativo: $VIRTUAL_ENV"
fi

# Instalar dependências
echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Verificar se o .env existe, senão criar a partir de env.txt
if [ ! -f .env ]; then
    echo "Criando .env a partir de env.txt..."
    cp env.txt .env
    echo "Por favor, configure as variáveis em .env (ex.: XAI_API_KEY)."
fi

# Criar diretório para modelos
mkdir -p models

# Testar importação de dependências principais
echo "Testando importação de dependências..."
python3 -c "import fastapi, pydantic, transformers, chromadb, web3" || {
    echo "Erro: Falha ao importar dependências. Verifique requirements.txt."
    exit 1
}

echo "Configuração concluída! Para iniciar a API, execute:"
echo "source .venv/bin/activate && uvicorn src.api.main:app --host 0.0.0.0 --port 8000"