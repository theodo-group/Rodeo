import typing

from utils.vertex_ai_service import VertexAIService


def generate_embedding(text_or_image: typing.Union[str, bytes]) -> list[float]:
    client = VertexAIService()
    return client.get_embedding(text_or_image)
