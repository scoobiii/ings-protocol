-- init_db.sql
-- Versão: 1.0.5
-- Responsabilidade: Inicialização das tabelas PostgreSQL para o INGS Protocol
-- Data: 2025-04-23
-- Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

-- Criação da tabela personas
CREATE TABLE IF NOT EXISTS personas (
    persona_id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(50),
    model_type VARCHAR(50),
    wallet_address VARCHAR(42),
    created_at BIGINT
);

-- Criação da tabela interactions
CREATE TABLE IF NOT EXISTS interactions (
    id SERIAL PRIMARY KEY,
    persona_id VARCHAR(100) REFERENCES personas(persona_id),
    message TEXT,
    response TEXT,
    mode VARCHAR(50),
    timestamp BIGINT
);

-- Criação da tabela sessions
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(100) PRIMARY KEY,
    persona_id VARCHAR(100) REFERENCES personas(persona_id),
    created_at BIGINT,
    expires_at BIGINT
);

-- Inserção de dados de exemplo
INSERT INTO personas (persona_id, name, model_type, wallet_address, created_at)
VALUES ('did:nings:artificial:llm:techlead:v2.0:k7p3l9n2m8o1', 'TechLead', 'mistral_local', '0x7890...1234', 1745088000)
ON CONFLICT DO NOTHING;