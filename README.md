# INGS Protocol

O INGS Protocol é um sistema distribuído para interações NxN entre personas de IA, com suporte a blockchain, banco vetorial, e validação ética.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/ings-protocol/ings-protocol.git
   cd ings-protocol
   ```

2. Configure o ambiente:
   ```bash
   ./scripts/setup.sh
   ```

3. Configure as variáveis de ambiente em `.env` (veja `env.txt`).

4. Implante com Docker:
   ```bash
   ./scripts/deploy.sh
   ```

## Uso

1. Crie uma persona:
   ```bash
   curl -X POST http://localhost:8000/handshake -d '{"persona_name":"TechLead","model_type":"mistral_local"}'
   ```

2. Interaja:
   ```bash
   curl -X POST http://localhost:8000/interact -d '{"persona_id":"did:nings:artificial:llm:techlead:v2.0:k7p3l9n2m8o1","message":"Hello","mode":"brainstorm"}'
   ```

## Dependências Não-Python

- **PostgreSQL**: Banco de dados para metadados.
  ```bash
  sudo apt install postgresql postgresql-contrib
  sudo -u postgres psql -c "CREATE DATABASE ings_db;"
  ```
- **Redis**: Cache para sessões.
  ```bash
  sudo apt install redis-server
  ```
- **Docker**: Contêineres.
  ```bash
  sudo apt install docker.io
  ```

## Testes

Execute:
```bash
./scripts/test.sh
```

## Documentação

Veja `docs/` para detalhes:
- `specification.md.txt`: Especificação técnica.
- `architecture-markdown.txt`: Arquitetura.
- `auto_tuning_guide.markdown.txt`: Tuning de modelos.

#### Contribuição

Leia CONTRIBUTING.md para diretrizes.
Crie issues ou pull requests no GitHub.
Junte-se ao canal Discord para colaboração.

### Rinha de Backend
O projeto inclui uma implementação para a Rinha de Backend 2023-Q3, 
- 1 otimizada com FastAPI, PostgreSQL e Redis. Veja detalhes em rinha-backend/.
- 2 redesenho de bash para bash++ nos top5

#### Licença
Creative Commons AI 4.0


Contato

### README.md
### Versão: 1.0.5
### Responsabilidade: Documentação inicial do INGS Protocol
### Data: 2025-04-23
### Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

Repositório: https://github.com/INGS-Protocol/ings-protocol


