from image_search.utils.generate_embedding import generate_embedding
from image_search.utils.get_supabase_client import get_supabase_client


def get_nearest_images(text_query: str, k: int = 4) -> list[dict]:
    """Get the nearest documents from the database given a text query.

    Args:
        text_query (str): The text query to use to find the nearest documents.
        k (int, optional): The number of nearest documents to return. Defaults to 4.

    Returns:
        list[dict]: A list of the nearest documents.
    """

    embedding = generate_embedding(text_query)
    supabase_client = get_supabase_client()
    response = supabase_client.rpc(
        "match_vectors",
        {
            "query_embedding": embedding,
            "match_count": k,
        },
    ).execute()
    return response.data
