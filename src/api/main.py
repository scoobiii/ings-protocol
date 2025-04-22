# main.py
# Versão: 1.0.5
# Responsabilidade: Ponto de entrada da API RESTful do INGS Protocol, inicializa o servidor FastAPI
# Data: 2025-04-22
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
from src.api.endpoints import handshake, interact, model_management, tuning, session
from src.utils.api_key import verify_api_key
import asyncpg
import redis.asyncio as redis
from chromadb import Client as ChromaClient
from typing import Optional

app = FastAPI(
    title="INGS Protocol API",
    version="1.0.5",
    description="API for managing INGS personas, interactions, tuning, and NxN sessions"
)

# Configuração de autenticação
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if not api_key or not await verify_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key

# Inicialização de conexões
async def init_db():
    app.state.postgres_pool = await asyncpg.create_pool(
        dsn="postgresql://user:password@localhost:5432/ings_db"
    )
    app.state.redis = redis.Redis(host="localhost", port=6379, decode_responses=True)
    app.state.chroma = ChromaClient(host="localhost", port=8001)

# Rotas
app.include_router(handshake.router, prefix="/handshake", tags=["Handshake"])
app.include_router(interact.router, prefix="/interact", tags=["Interaction"])
app.include_router(model_management.router, prefix="/models", tags=["Model Management"])
app.include_router(tuning.router, prefix="/tune", tags=["Tuning"])
app.include_router(session.router, prefix="/session", tags=["NxN Session"])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.postgres_pool.close()
    await app.state.redis.close()

@app.get("/")
async def root():
    return {"message": "INGS Protocol API v1.0.5"}

# Nota sobre Bend:
# Em Bend, o servidor API seria substituído por uma função funcional que processa
# requisições HTTP em paralelo, possivelmente usando um runtime HTTP customizado.
# Exemplo: `def handle_request(req: HttpRequest) -> HttpResponse`
# O paralelismo seria útil para NxN, mas exigiria reimplementar FastAPI.