```bash
#!/bin/bash
# deploy.sh
# Versão: 1.0.4
# Responsabilidade: Implantar o projeto INGS em produção com Docker
# Data: 2025-04-21
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

set -e

echo "Iniciando deploy do INGS Protocol..."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Erro: Docker não está instalado. Instale-o antes de continuar."
    exit 1
fi

# Verificar se o .env existe
if [ ! -f .env ]; then
    echo "Erro: Arquivo .env não encontrado. Copie .env.example para .env e configure as variáveis."
    exit 1
fi

# Construir a imagem Docker
echo "Construindo imagem Docker..."
docker build -t ings-protocol:1.0.4 .

# Parar e remover container existente (se houver)
if [ "$(docker ps -q -f name=ings-protocol)" ]; then
    echo "Parando container existente..."
    docker stop ings-protocol
fi
if [ "$(docker ps -a -q -f name=ings-protocol)" ]; then
    echo "Removendo container existente..."
    docker rm ings-protocol
fi

# Iniciar o container
echo "Iniciando container..."
docker run -d \
    --name ings-protocol \
    -p 8000:8000 \
    --env-file .env \
    -v $(pwd)/models:/app/models \
    ings-protocol:1.0.4

echo "Deploy concluído! A API está rodando em http://localhost:8000"
echo "Acesse a documentação em http://localhost:8000/docs"
```