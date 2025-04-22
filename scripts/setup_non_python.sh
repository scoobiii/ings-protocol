#!/bin/bash
# setup_non_python.sh
# Versão: 1.0.5
# Responsabilidade: Instalar dependências não-Python para o INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

echo "Instalando dependências não-Python para o INGS Protocol..."

# Verificar espaço em disco
echo "Espaço em disco antes da instalação:"
df -h /

# Atualizar pacotes
sudo apt update

# Instalar PostgreSQL
echo "Instalando PostgreSQL..."
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo -u postgres psql -c "CREATE DATABASE ings_db;" || true
sudo -u postgres psql -c "CREATE USER ings_user WITH PASSWORD 'secure_password';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ings_db TO ings_user;" || true
psql -U ings_user -d ings_db -f scripts/init_db.sql || {
    echo "Erro: Falha ao executar init_db.sql. Verifique o arquivo."
    exit 1
}

# Otimizar PostgreSQL para 8 GB RAM
echo "Otimizando PostgreSQL..."
sudo sed -i 's/#shared_buffers = .*/shared_buffers = 128MB/' /etc/postgresql/*/main/postgresql.conf
sudo sed -i 's/#work_mem = .*/work_mem = 4MB/' /etc/postgresql/*/main/postgresql.conf
sudo systemctl restart postgresql

# Instalar Redis
echo "Instalando Redis..."
sudo apt install -y redis-server
sudo systemctl start redis
sudo systemctl enable redis

# Otimizar Redis para 8 GB RAM
echo "Otimizando Redis..."
sudo bash -c 'echo "maxmemory 256mb" >> /etc/redis/redis.conf'
sudo bash -c 'echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf'
sudo systemctl restart redis

# Instalar Docker
echo "Instalando Docker..."
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# Instalar Solidity (solc e Hardhat)
echo "Instalando Solidity..."
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:ethereum/ethereum
sudo apt update
sudo apt install -y solc
sudo apt install -y nodejs npm
npm install -g hardhat

# Limpar cache do apt
echo "Limpando cache do apt..."
sudo apt-get clean
sudo apt-get autoclean

# Verificar espaço em disco
echo "Espaço em disco após a instalação:"
df -h /

echo "Instalação concluída! Faça logout e login para aplicar o grupo Docker."
echo "Para validar, execute:"
echo "./scripts/validate_non_python.sh"
echo "Para continuar com dependências Python, execute:"
echo "source .venv/bin/activate && ./scripts/setup.sh"