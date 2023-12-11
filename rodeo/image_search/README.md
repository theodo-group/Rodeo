## Vectors based image search app

### Installation:

1. Duplicate copy .env.example to .env and fill in the values

2. Run below query on Supabase

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS vectors (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1408)
);
CREATE OR REPLACE FUNCTION match_vectors(query_embedding VECTOR(1408), match_count INT)
RETURNS TABLE(
    id UUID,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1408),
    similarity FLOAT
) LANGUAGE plpgsql AS $$
#variable_conflict use_column
BEGIN
    RETURN QUERY
    SELECT
        vectors.id,
        vectors.content,
        vectors.metadata,
        vectors.embedding,
        1 - (vectors.embedding <=> query_embedding) AS similarity
    FROM
        vectors
    ORDER BY
        vectors.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the app

```bash
streamlit run streamlit_app
```