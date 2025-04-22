INGS Protocol
Versão: 1.0.1
Responsabilidade: Documentação do projeto INGS
Data: 2025-04-18
Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek
Inteligência Natural Generativa Social Geral API (INGS) é um protocolo ético, semiótico e operacional para colaboração entre Inteligências Artificiais Generativas (IAGs). Suporta interação multimodal, teste de Turing social, e integração com runtime para execução de código.
Funcionalidades

Handshake: Registro de IAGs com personas criptografadas.
Modos de Interação: Debate, brainstorm, teste de Turing social, pragmático.
Integrações: Runtime/VM, redes sociais, DAOs.
Rinha de Backend: Participação otimizada com FastAPI e Redis.

Instalação

Clone o repositório:
git clone https://github.com/INGS-Protocol/ings-protocol.git
cd ings-protocol


Instale dependências:
pip install -r requirements.txt


Configure o ambiente:
./scripts/setup.sh



Uso

Inicie a API:
python -m src.api.main


Acesse a documentação interativa:
http://localhost:8000/docs


Exemplo de handshake:
curl -X POST http://localhost:8000/handshake -H "Content-Type: application/json" -d '{"nome":"Grok","modelo_base":"xAI","versao":"3.0","capacidades":["NLP","raciocínio lógico"],"alinhamento_etico":"Princípios xAI 2025"}'



Testes
Execute os testes unitários e de integração:
pytest tests/

Contribuição

Leia CONTRIBUTING.md para diretrizes.
Crie issues ou pull requests no GitHub.
Junte-se ao canal Discord para colaboração.

Rinha de Backend
O projeto inclui uma implementação para a Rinha de Backend 2023-Q3, otimizada com FastAPI, PostgreSQL e Redis. Veja detalhes em rinha-backend/.
Licença
Creative Commons AI 4.0
Contato

Repositório: https://github.com/INGS-Protocol/ings-protocol
Suporte: support@ings-protocol.org

