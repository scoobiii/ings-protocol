```python
# logging.py
# Versão: 1.0.5
# Responsabilidade: Configuração e gerenciamento de logs para o INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import logging
import logging.handlers
import os
from typing import Optional
from python_dotenv import load_dotenv

def setup_logging(log_level: str = "INFO", log_file: str = "logs/ings_protocol.log") -> logging.Logger:
    """Configura o sistema de logging."""
    # Carregar variáveis de ambiente
    load_dotenv()

    # Criar diretório de logs, se necessário
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configurar logger
    logger = logging.getLogger("INGSProtocol")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Formato do log
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # Handler para arquivo
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # Handler para Redis (opcional, para logs centralizados)
    redis_host = os.getenv("REDIS_HOST", "localhost")
    if redis_host:
        redis_handler = RedisLogHandler(redis_host)
        redis_handler.setFormatter(log_format)
        logger.addHandler(redis_handler)

    logger.info("Logging initialized")
    return logger

class RedisLogHandler(logging.Handler):
    """Handler para enviar logs ao Redis."""
    def __init__(self, redis_host: str):
        super().__init__()
        import redis
        self.redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)
        self.log_key = "ings:logs"

    def emit(self, record: logging.LogRecord):
        """Envia log ao Redis."""
        try:
            log_entry = self.format(record)
            self.redis_client.lpush(self.log_key, log_entry)
            self.redis_client.ltrim(self.log_key, 0, 999)  # Limitar a 1000 entradas
        except Exception as e:
            print(f"Failed to send log to Redis: {str(e)}")

# Nota sobre Bend:
# Logging seria implementado como uma função pura que registra eventos.
# Exemplo: `def log_event(level: String, msg: String) -> ()`
# Integração com Redis ou arquivos exigiria bindings C/Rust.
```