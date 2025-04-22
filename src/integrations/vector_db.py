# vector_db.py
# Versão: 1.0.5
# Responsabilidade: Integração com banco vetorial (ChromaDB) no INGS Protocol
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import logging
import chromadb
from typing import List, Dict, Any
from src.protocols.vector_compression import VectorCompressor

class VectorDBIntegration:
    def __init__(self, collection_name: str = "ings_embeddings"):
        """Inicializa a integração com ChromaDB."""
        self.logger = logging.getLogger(__name__)
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(collection_name, get_or_create=True)
        self.compressor = VectorCompressor()

    def store_embeddings(self, texts: List[str], metadata: List[Dict[str, Any]]) -> None:
        """Armazena embeddings no banco vetorial."""
        try:
            embeddings = self.compressor.compress(texts)
            ids = [f"embedding_{i}" for i in range(len(texts))]
            self.collection.add(embeddings=embeddings.tolist(), metadatas=metadata, ids=ids)
            self.logger.info(f"Stored {len(texts)} embeddings in collection {self.collection.name}")
        except Exception as e:
            self.logger.error(f"Failed to store embeddings: {str(e)}")
            raise

    def query_embeddings(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Consulta embeddings semelhantes."""
        try:
            query_embedding = self.compressor.compress([query_text])[0].tolist()
            results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
            self.logger.info(f"Queried {n_results} embeddings for query: {query_text}")
            return results["metadatas"][0]
        except Exception as e:
            self.logger.error(f"Failed to query embeddings: {str(e)}")
            raise