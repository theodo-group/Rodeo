from utils.vertex_ai_service import VertexAIService


def generate_image(prompt: str) -> bytes:
    client = VertexAIService()
    return client.generate_image(prompt)
