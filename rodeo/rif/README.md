# Welcome to Rodeo Image Finder (RIF) 🚀🤖

## What is RIF?

RIF allows you to find similar images in a huge dataset through a simple text query.

## How does it work?

Upload your images and then ask questions about them. RIF will then find the most similar images in your dataset.

## How to Run RIF

RIF is a Streamlit app that uses Supabase as a database.

### Installation

1. Duplicate copy `.env.example` to `.env` and fill in the values

2. Run below query on Supabase console to create the table and function needed for RIF

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