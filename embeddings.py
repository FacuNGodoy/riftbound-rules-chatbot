"""Embeddings por API de Gemini.

El servidor no carga ningún modelo: el plan gratuito de Render tiene 512 MB y
sentence-transformers se trae PyTorch, que solo ya no entra. El índice se
construye con ingest.py y se versiona; en producción cada pregunta gasta un
embedding de la API.
"""
from chromadb.utils import embedding_functions

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768


def make_embedding_function():
    return embedding_functions.GoogleGenaiEmbeddingFunction(
        api_key_env_var="GEMINI_API_KEY",
        model_name=EMBEDDING_MODEL,
        dimension=EMBEDDING_DIMENSION,
    )
