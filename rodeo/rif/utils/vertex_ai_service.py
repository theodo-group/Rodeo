import base64
import os
import typing

from google.cloud import aiplatform
from google.protobuf import struct_pb2


class VertexAIService:
    def __init__(
        self,
        location: str = "us-central1",
        api_regional_endpoint: str = "us-central1-aiplatform.googleapis.com",
    ):
        client_options = {"api_endpoint": api_regional_endpoint}
        self.client = aiplatform.gapic.PredictionServiceClient(
            client_options=client_options,
        )
        self.location = location
        self.project = os.getenv("PROJECT_ID")

    def get_embedding(self, text_or_image: typing.Union[str, bytes]) -> list[float]:
        instance = struct_pb2.Struct()
        is_text = isinstance(text_or_image, str)

        if is_text:
            instance.fields["text"].string_value = text_or_image

        if isinstance(text_or_image, bytes):
            encoded_content = base64.b64encode(text_or_image).decode("utf-8")
            image_struct = instance.fields["image"].struct_value
            image_struct.fields["bytesBase64Encoded"].string_value = encoded_content

        endpoint = (
            f"projects/{self.project}/locations/{self.location}"
            "/publishers/google/models/multimodalembedding@001"
        )
        response = self.client.predict(endpoint=endpoint, instances=[instance])
        embedding = None
        if is_text:
            text_emb_value = response.predictions[0]["textEmbedding"]
            embedding = [v for v in text_emb_value]
        else:
            image_emb_value = response.predictions[0]["imageEmbedding"]
            embedding = [v for v in image_emb_value]

        return embedding

    def generate_image(self, textual_prompt: str) -> bytes:
        image_gen_endpoint = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{self.project}/locations/{self.location}/publishers/google/models/imagegeneration:predict"

        instance = {"prompt": textual_prompt}
        parameters = {"sampleCount": 1}

        response = self.client.predict(
            endpoint=image_gen_endpoint,
            instances=[instance],
            parameters=parameters,
        )

        generated_image = response.predictions[0]["output"]

        return generated_image
