# Auto-Tuning Guide for INGS Protocol
# Versão: 1.0.4
# Responsabilidade: Guia para auto-tuning e aprendizado incremental
# Data: 2025-04-21
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

## Introdução
O INGS Protocol suporta auto-tuning de modelos usando LoRA (Low-Rank Adaptation) e memória incremental com ChromaDB. Este guia explica como ajustar modelos para personalização contínua.

## Pré-requisitos
- Python 3.9+
- Dependências: `peft`, `chromadb`, `sentence-transformers`.
- Modelo base (ex.: LLaMA 3.1, Mistral 7B).

## Configuração
1. **Instale dependências**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure o .env**:
   ```bash
   cp .env.example .env
   ```
   Edite `.env`:
   ```
   CHROMADB_HOST=localhost
   CHROMADB_PORT=8001
   HUGGINGFACE_TOKEN=your_hf_token
   ```

## Uso
1. **Inicie a API**:
   ```bash
   python -m src.api.main
   ```
2. **Crie uma persona**:
   Use um JSON como `examples/personas/techlead_ings.json`:
   ```bash
   curl -X POST http://localhost:8000/handshake -H "Content-Type: application/json" -d @examples/personas/techlead_ings.json
   ```
3. **Ajuste o modelo**:
   Envie dados de treinamento via `/tune`:
   ```bash
   curl -X POST http://localhost:8000/tune -H "Content-Type: application/json" -d '{"persona_id":"did:nings:artificial:llm:techlead:v2.0:a7f3b9d2c8e1","training_data":[{"input":"Explain DevOps","output":"DevOps is a set of practices..."}],"lora_config":{"model_name":"meta-llama/Llama-3.1-8B","rank":8,"alpha":16}}'
   ```
4. **Memória Incremental**:
   Interações são automaticamente armazenadas no ChromaDB para aprendizado contextual.

## Dicas
- **LoRA Config**:
  - `rank`: 8 para modelos pequenos, 16 para grandes.
  - `alpha`: 16 para equilíbrio entre adaptação e estabilidade.
- **Tamanho dos Dados**: Use pelo menos 10 exemplos para tuning inicial.
- **ChromaDB**: Configure `CHROMADB_HOST` para servidores remotos, se necessário.

## Solução de Problemas
- **Erro de Convergência**: Reduza `rank` ou aumente `alpha`.
- **Erro de Memória**: Use modelos menores ou quantização.

Veja mais em [architecture.md](../architecture.md).