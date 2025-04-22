```python
# grpc_server.py
# Versão: 1.0.5
# Responsabilidade: Servidor gRPC para integração do Orchestrator com a API FastAPI
# Data: 2025-04-23
# Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

import grpc
from concurrent import futures
import proto.ingsxings_pb2 as ingsxings_pb2
import proto.ingsxings_pb2_grpc as ingsxings_pb2_grpc
from src.orchestrator.manager import Orchestrator
from src.api.models.session import SessionCreateInput, SessionMessageInput

class INGSxINGSService(ingsxings_pb2_grpc.INGSxINGSServiceServicer):
    def __init__(self):
        """Inicializa o serviço gRPC com o Orchestrator."""
        self.orchestrator = Orchestrator(
            postgres_dsn="postgresql://user:password@localhost:5432/ings_db",
            redis_host="localhost",
            chromadb_host="localhost"
        )

    async def CreateSession(self, request, context):
        """Cria uma sessão NxN via gRPC."""
        session_input = SessionCreateInput(
            participants=request.participants,
            session_rules={"mode": request.rules.mode, "max_turns": request.rules.max_turns}
        )
        session_id = await self.orchestrator.create_session(session_input)
        return ingsxings_pb2.SessionResponse(session_id=session_id)

    async def SendMessage(self, request, context):
        """Envia uma mensagem para a sessão."""
        message_input = SessionMessageInput(sender_id=request.sender_id, message_data=request.message_data)
        responses = await self.orchestrator.send_message(request.session_id, message_input)
        return ingsxings_pb2.MessageResponse(responses=responses)

def serve():
    """Inicia o servidor gRPC."""
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    ingsxings_pb2_grpc.add_INGSxINGSServiceServicer_to_server(INGSxINGSService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

# Nota sobre Bend:
# Em Bend, o gRPC seria substituído por uma função funcional para comunicação.
# Exemplo: `def handle_grpc_request(req: GrpcRequest) -> GrpcResponse`
# O paralelismo seria aplicado a chamadas NxN, mas gRPC exigiria bindings.
```