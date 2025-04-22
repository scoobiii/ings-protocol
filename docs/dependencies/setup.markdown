# dependencies_setup.markdown
# Versão: 1.0.5
# Responsabilidade: Guia de instalação e testes de dependências não-Python no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

# Configuração de Dependências Não-Python

## PostgreSQL
**Função**: Armazena metadados de personas e sessões (`src/orchestrator/session.py`).

**Instalação (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres psql -c "CREATE DATABASE ings_db;"
sudo -u postgres psql -c "CREATE USER ings_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ings_db TO ings_user;"
```

**Testes**: Validados indiretamente por `tests/integration/test_api.py` (endpoints `/handshake`, `/interact`).

**Integração**: Conectado via Python (`psycopg2` ou `sqlalchemy`, implícito).

## Redis
**Função**: Cache para sessões (`src/orchestrator/session.py`).

**Instalação (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

**Testes**: Validados indiretamente por `tests/integration/test_api.py`.

**Integração**: Acessado via `redis-py` (implícito em `requirements.txt`).

## Docker
**Função**: Implantação do projeto (`scripts/deploy.sh`, `Dockerfile`).

**Instalação (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

**Testes**: Verificado por `scripts/deploy.sh` (construção/execução do contêiner).

**Integração**: Orquestra Python e dependências via `Dockerfile`.

## Solidity (Blockchain)
**Função**: Suporte a carteiras e auditoria (`src/integrations/blockchain.py`, `contracts/INGSRegistry.sol`).

**Instalação**:
```bash
# Instalar solc
sudo apt install solc
# Ou usar Hardhat
npm install -g hardhat
```

**Testes**: Não implementado. Recomenda-se Hardhat para testes de contratos.

**Integração**: Python (`web3.py` em `requirements.txt`) interage com contratos via Ethereum.

## Bend (Não Usado)
**Esclarecimento**: Bend não é uma dependência do projeto. Se mencionado, foi um erro. Não está no `tree` ou `requirements.txt`.

**Instalação (Hipotética)**:
```bash
git clone https://github.com/HigherOrderCO/Bend
cd Bend
cargo build --release
```

**Testes**: Não aplicável.

**Integração**: Poderia ser chamado via Python (`subprocess.run()`), mas não é usado.

## Notas
- Veja `docs/specification.md.txt` e `docs/architecture-markdown.txt` para detalhes da arquitetura.
- Configurações em `env.txt` (ex.: `POSTGRES_HOST`, `REDIS_HOST`).
- Execute `scripts/setup.sh` para dependências Python e `scripts/deploy.sh` para Docker.