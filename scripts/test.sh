#!/bin/bash
# test.sh
# Versão: 1.0.4
# Responsabilidade: Executar testes unitários e de integração
# Data: 2025-04-21
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

echo "Executando testes do INGS Protocol..."

# Verificar se o ambiente virtual existe e ativá-lo
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Erro: Ambiente virtual não encontrado. Execute setup.sh primeiro."
    exit 1
fi

# Verificar se pytest está instalado
if ! command -v pytest &> /dev/null; then
    echo "Erro: pytest não está instalado. Verifique requirements.txt."
    exit 1
fi

# Executar testes unitários
echo "Executando testes unitários..."
pytest tests/unit/ -v

# Executar testes de integração
echo "Executando testes de integração..."
pytest tests/integration/ -v

# Executar testes de Turing social
echo "Executando testes de Turing social..."
pytest tests/social_turing/ -v

echo "Testes concluídos com sucesso!"