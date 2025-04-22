import os

# Diretório raiz da pasta docs
DOCS_DIR = "docs"
OUTPUT_FILE = "docs-all-files.txt"

# Lista de arquivos na pasta docs (Mantida igual, pois os arquivos foram atualizados in-place)
# Se novos arquivos fossem criados (ex: nxn_collaboration_guide.markdown), seriam adicionados aqui.
FILES = [
    "docs/api-spec.yaml",
    "docs/architecture.markdown",
    "docs/auto_tuning_guide.markdown",
    "docs/manifesto.markdown",
    "docs/offline_model_setup.markdown",
    "docs/online_model_usage.markdown",
    "docs/specification.md"
]

# Função para inferir a responsabilidade do arquivo
def get_responsibility(file_path):
    # Responsabilidades atualizadas refletindo o conteúdo pós-NxN
    responsibilities = {
        "docs/api-spec.yaml": "Especificação OpenAPI/Swagger da API INGS, incluindo endpoints /handshake, /interact, /tune e /session (para NxN).",
        "docs/architecture.markdown": "Descreve a arquitetura técnica do INGS Protocol, incluindo o Orchestrator para interações NxN.",
        "docs/auto_tuning_guide.markdown": "Guia para fine-tuning (LoRA) e memória incremental (ChromaDB) aplicados a personas INGS.",
        "docs/manifesto.markdown": "Declara a visão e princípios do INGS Protocol, incluindo colaboração multi-agente (NxN).",
        "docs/offline_model_setup.markdown": "Instruções para configurar modelos offline (LLaMA, Mistral) como personas INGS.",
        "docs/online_model_usage.markdown": "Guia para usar modelos online (Grok, Qwen) como personas INGS via API.",
        "docs/specification.md": "Especificação técnica detalhada do INGS Protocol v1.0.5, cobrindo todos os aspectos, incluindo interações NxN."
        # Adicionar aqui se houver novos arquivos:
        # "docs/nxn_collaboration_guide.markdown": "Guia detalhado sobre como configurar e executar sessões colaborativas NxN."
    }
    return responsibilities.get(file_path, "Função não documentada.")

# Função para gerar um esboço de conteúdo (placeholder) - Mantida como antes
# Na prática, este script seria usado para *ler* os arquivos reais, não gerar placeholders.
# Se fosse para gerar placeholders, a lógica seria a mesma.
def generate_placeholder_content(file_path):
    # Apenas como exemplo, mantendo a lógica original do script
    if file_path.endswith(".yaml"):
        return (
            f"# {file_path}\n"
            f"# Esboço de especificação YAML (v1.0.5)\n"
            f"openapi: 3.1.0\n" # Usando versão mais recente
            f"info:\n"
            f"  title: INGS Protocol API\n"
            f"  version: 1.0.5\n"
            f"paths:\n"
            f"  /handshake:\n"
            f"    post:\n"
            f"      summary: Cria uma Persona INGS\n"
            f"      # ... mais detalhes ...\n"
            f"  /interact:\n"
            f"    post:\n"
            f"      summary: Interação 1x1, 1xN, Nx1\n"
            f"      # ... mais detalhes ...\n"
            f"  /tune:\n"
            f"    post:\n"
            f"      summary: Inicia fine-tuning LoRA\n"
            f"      # ... mais detalhes ...\n"
            f"  /session/create:\n"
            f"    post:\n"
            f"      summary: Cria uma sessão NxN\n"
            f"      # ... mais detalhes ...\n"
            # ... outros endpoints /session ...
        )
    elif file_path.endswith(".md") or file_path.endswith(".markdown"):
        return (
            f"# {file_path}\n"
            f"# Versão: 1.0.5\n"
            f"\n"
            f"## Introdução\n"
            f"Este é um esboço para o documento {file_path}.\n"
            f"Conteúdo detalhado será adicionado posteriormente, alinhado com a v1.0.5 (NxN).\n"
            f"\n"
            f"## Seções\n"
            f"- Seção 1: TBD (Considerando NxN)\n"
            f"- Seção 2: TBD (Considerando NxN)"
        )
    return f"Placeholder para {file_path} (v1.0.5)\nConteúdo não implementado."

# Função para criar o arquivão único
def create_single_file(use_real_files=True): # Adicionado parâmetro para clareza
    # Criar diretório 'docs' se não existir (para o script rodar sem erro)
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        # Criar arquivos vazios para evitar FileNotFoundError se use_real_files=True
        for file_path in FILES:
             # Garante que subdiretórios existam se necessário
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# Placeholder inicial para {file_path}\n")


    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for file_path in FILES:
            # Cabeçalho atualizado
            header = (
                f"--- Arquivo: {file_path} ---\n"
                f"Versão: 1.0.5\n" # Versão atualizada
                f"Responsabilidade: {get_responsibility(file_path)}\n"
                # Mantendo a assinatura original do script, pode ser alterada
                f"Assinatura: Gerado por Script (Originalmente por Grok 3, xAI)\n"
                f"--- Conteúdo ---\n"
            )
            outfile.write(header)

            # Ler conteúdo real ou gerar placeholder
            content = ""
            if use_real_files and os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                except Exception as e:
                    content = f"# ERRO AO LER ARQUIVO {file_path}: {e}\n"
                    content += generate_placeholder_content(file_path) # Fallback
            else:
                 content = generate_placeholder_content(file_path) # Gerar placeholder

            outfile.write(content)
            outfile.write("\n\n--- Fim do Arquivo ---\n\n")

if __name__ == "__main__":
    # Por padrão, tenta ler os arquivos reais da pasta 'docs/'
    # Se quiser gerar apenas placeholders, chame create_single_file(use_real_files=False)
    create_single_file(use_real_files=True)
    print(f"Arquivão único '{OUTPUT_FILE}' gerado/atualizado (v1.0.5).")
    print("Nota: Este script tentará ler os arquivos reais listados em 'FILES'.")
    print("Se os arquivos não existirem ou houver erro, placeholders serão usados.")