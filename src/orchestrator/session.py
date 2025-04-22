```python
# session.py
# Versão: 1.0.5
# Responsabilidade: Modelos e funções para gerenciamento de sessões NxN
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

from pydantic import BaseModel
from typing import List, Dict, Any
import asyncpg

class SessionModel(BaseModel):
    session_id: str
    participants: List[str]
    rules: Dict[str, Any]
    status: str

async def save_session(pool: asyncpg.Pool, session: SessionModel):
    """Salva o estado de uma sessão no banco."""
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO sessions (session_id, participants, rules, status)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (session_id) DO UPDATE
            SET participants = $2, rules = $3, status = $4
            """,
            session.session_id, session.participants, session.rules, session.status
        )

async def load_session(pool: asyncpg.Pool, session_id: str) -> SessionModel:
    """Carrega uma sessão do banco."""
    async with pool.acquire() as conn:
        session = await conn.fetchrow(
            "SELECT session_id, participants, rules, status FROM sessions WHERE session_id = $1",
            session_id
        )
        if not session:
            raise ValueError(f"Session {session_id} not found")
        return SessionModel(**session)

# Nota sobre Bend:
# Sessões seriam tipos algébricos imutáveis.
# Exemplo: `data Session = Active { id: String, participants: List<String>, rules: Rules } | Terminated`
# Persistência exigiria bindings para PostgreSQL.
```