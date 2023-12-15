import os

from google.cloud import aiplatform


class Movie:
    name: str
    description: str


class VertexChatClient:
    def __init__(
        self,
        location: str = "us-central1",
        api_regional_endpoint: str = "us-central1-aiplatform.googleapis.com",
    ):
        client_options = {"api_endpoint": api_regional_endpoint}
        self.client = aiplatform.gapic.PredictionServiceClient(
            client_options=client_options
        )
        self.location = location
        # self.project = os.getenv("PROJECT_ID")
        self.project = "hackaton-2-406607"

    def generate_movie(self) -> str:
        endpoint = (
            f"projects/{self.project}/locations/{self.location}"
            "publishers/google/models/text-bison@002"
        )
        response = self.client.predict(endpoint=endpoint)
        print(response.predictions[0])
        return response.predictions[0]


def generate_movie() -> Movie:
    client = VertexChatClient()
    return client.generate_movie()
