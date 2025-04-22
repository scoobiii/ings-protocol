#!/bin/bash
# fix_postgres.sh
# Versão: 1.0.8
# Responsabilidade: Corrigir instalação e configuração do PostgreSQL para o INGS Protocol
# Data: 2025-04-21
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

echo "Corrigindo PostgreSQL para o INGS Protocol..."

# Verificar espaço em disco
echo "Espaço em disco antes da correção:"
df -h /

# Verificar se o PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo "PostgreSQL não está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib
fi

# Obter versão instalada do PostgreSQL
PG_VERSION=$(pg_lsclusters | awk 'NR==1 {print $1}')
if [ -z "$PG_VERSION" ] || [ "$PG_VERSION" = "Ver" ]; then
    PG_VERSION=$(pg_lsclusters | awk 'NR==2 {print $1}')
fi

if [ -z "$PG_VERSION" ] || [ "$PG_VERSION" = "Ver" ]; then
    echo "Erro: Não foi possível determinar a versão do PostgreSQL."
    exit 1
fi

echo "Versão do PostgreSQL detectada: $PG_VERSION"

# Verificar status do cluster
CLUSTER_STATUS=$(pg_lsclusters | awk 'NR>1 {print $4}' | head -1)
if [ "$CLUSTER_STATUS" != "online" ]; then
    echo "Cluster PostgreSQL não está online. Iniciando..."
    sudo pg_ctlcluster $PG_VERSION main start
fi

# Verificar status real do PostgreSQL
echo "Verificando status do PostgreSQL..."
if ! systemctl is-active --quiet postgresql; then
    echo "PostgreSQL não está rodando. Tentando iniciar..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Corrigir permissões do socket
echo "Corrigindo permissões do socket..."
sudo mkdir -p /var/run/postgresql
sudo chown postgres:postgres /var/run/postgresql
sudo chmod 755 /var/run/postgresql

# Configurar postgresql.conf
echo "Configurando postgresql.conf..."
POSTGRES_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
if [ ! -f "$POSTGRES_CONF" ]; then
    echo "Erro: Arquivo postgresql.conf não encontrado em $POSTGRES_CONF"
    exit 1
fi

sudo sed -i "s/#listen_addresses = .*/listen_addresses = 'localhost'/" "$POSTGRES_CONF"
sudo sed -i "s/#port = .*/port = 5432/" "$POSTGRES_CONF"
sudo sed -i "s/#unix_socket_directories = .*/unix_socket_directories = '\/var\/run\/postgresql'/" "$POSTGRES_CONF"

# Configurar pg_hba.conf
echo "Configurando pg_hba.conf..."
PG_HBA_CONF="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
if [ ! -f "$PG_HBA_CONF" ]; then
    echo "Erro: Arquivo pg_hba.conf não encontrado em $PG_HBA_CONF"
    exit 1
fi

sudo bash -c "cat > $PG_HBA_CONF << EOF
local   all   postgres   peer
local   all   all        md5
host    all   all        127.0.0.1/32  md5
EOF"

# Reiniciar PostgreSQL
echo "Reiniciando PostgreSQL..."
sudo systemctl restart postgresql

# Esperar o PostgreSQL estar pronto
for i in {1..10}; do
    if sudo -u postgres psql -c "SELECT 1;" &> /dev/null; then
        break
    fi
    echo "Aguardando PostgreSQL iniciar... ($i/10)"
    sleep 2
done

# Recriar banco e usuário
echo "Recriando banco e usuário..."
sudo -u postgres psql -c "DROP DATABASE IF EXISTS ings_db;" || true
sudo -u postgres psql -c "DROP USER IF EXISTS ings_user;" || true
sudo -u postgres psql -c "CREATE USER ings_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "CREATE DATABASE ings_db OWNER ings_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ings_db TO ings_user;"

# Verificar conexão
echo "Testando conexão..."
psql -U ings_user -d ings_db -h 127.0.0.1 -c "SELECT 1;" || {
    echo "Erro: Falha ao conectar ao banco. Verifique logs (sudo journalctl -u postgresql)."
    exit 1
}

# Verificar espaço em disco
echo "Espaço em disco após a correção:"
df -h /

echo "PostgreSQL corrigido e configurado com sucesso!"


