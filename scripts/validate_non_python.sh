#!/bin/bash
# validate_non_python.sh
# Versão: 1.0.5
# Responsabilidade: Validar dependências não-Python para o INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

echo "Validando dependências não-Python..."

# Verificar PostgreSQL
echo "Testando PostgreSQL..."
if ! psql -U ings_user -d ings_db -c "SELECT * FROM personas;" > /dev/null 2>&1; then
    echo "Erro: Falha ao conectar ao PostgreSQL. Verifique scripts/init_db.sql e configurações."
    exit 1
fi
echo "PostgreSQL OK."

# Verificar Redis
echo "Testando Redis..."
if ! redis-cli ping | grep -q "PONG"; then
    echo "Erro: Falha ao conectar ao Redis. Verifique se está rodando (sudo systemctl start redis)."
    exit 1
fi
echo "Redis OK."

# Verificar Docker
echo "Testando Docker..."
if ! docker run --rm hello-world > /dev/null 2>&1; then
    echo "Erro: Falha ao executar Docker. Verifique instalação e permissões (sudo usermod -aG docker $USER)."
    exit 1
fi
echo "Docker OK."

# Verificar Solidity (solc)
echo "Testando Solidity (solc)..."
if ! solc --version > /dev/null 2>&1; then
    echo "Erro: Falha ao executar solc. Verifique instalação (sudo apt install solc)."
    exit 1
fi
echo "Solidity (solc) OK."

# Verificar Hardhat
echo "Testando Hardhat..."
if ! hardhat --version > /dev/null 2>&1; then
    echo "Erro: Falha ao executar Hardhat. Verifique instalação (npm install -g hardhat)."
    exit 1
fi
echo "Hardhat OK."

echo "Validação concluída! Todas as dependências não-Python estão funcionando."
echo "Para continuar com dependências Python, execute:"
echo "source .venv/bin/activate && ./scripts/setup.sh"