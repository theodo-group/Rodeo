from image_search.utils.get_supabase_client import get_supabase_client


def save_doc_and_embed(content: str, embedding: list[float]):
    response = (
        get_supabase_client()
        .table("vectors")
        .insert({"content": content, "embedding": embedding})
        .execute()
    )
    return response
