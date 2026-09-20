"""
Ingesta: lee los .md de docs/, los divide por secciones (## / ###)
y los indexa en ChromaDB con embeddings de la API de Gemini.

Se corre una sola vez y el índice resultante se versiona: el servidor de
producción no reindexa, solo consulta.
"""

import os
import re
import time
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from embeddings import make_embedding_function

# El free tier permite 100 textos por minuto. Con lotes chicos y una pausa
# entre lotes la ingesta entra sin chocar la cuota.
BATCH_SIZE = 20
PAUSE_SECONDS = 14

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"
COLLECTION_NAME = "riftbound_rules"

CATEGORY_MAP = {
    "core_rules": "rules",
    "01_core rules patch notes": "rules",
    "02_spiritforge rules patch notes": "rules",
    "03_unleash rules patch notes": "rules",
    "04_vendetta rules patch notes": "rules",
    "tournament_rules": "tournament",
    "constructed_format_legality": "legality",
    "2v2_constructed_legality": "legality",
}


def chunk_markdown(text: str, source: str) -> list[dict]:
    """Divide un markdown en chunks por secciones (## o ###)."""
    chunks = []
    current_header = source  # fallback
    current_lines = []

    for line in text.split("\n"):
        header_match = re.match(r"^(#{1,3})\s+(.+)", line)
        if header_match:
            # Guardar chunk anterior si tiene contenido
            content = "\n".join(current_lines).strip()
            if content and len(content) > 20:
                chunks.append({
                    "text": f"{current_header}\n\n{content}",
                    "header": current_header,
                    "source": source,
                })
            current_header = header_match.group(2).strip()
            current_lines = []
        else:
            current_lines.append(line)

    # Ultimo chunk
    content = "\n".join(current_lines).strip()
    if content and len(content) > 20:
        chunks.append({
            "text": f"{current_header}\n\n{content}",
            "header": current_header,
            "source": source,
        })

    return chunks


def split_large_chunks(chunks: list[dict], max_chars: int = 1500) -> list[dict]:
    """Divide chunks demasiado grandes en sub-chunks."""
    result = []
    for chunk in chunks:
        text = chunk["text"]
        if len(text) <= max_chars:
            result.append(chunk)
            continue

        # Dividir por lineas vacias (parrafos)
        paragraphs = re.split(r"\n\n+", text)
        current = []
        current_len = 0

        for para in paragraphs:
            if current_len + len(para) > max_chars and current:
                result.append({
                    "text": "\n\n".join(current),
                    "header": chunk["header"],
                    "source": chunk["source"],
                })
                current = [para]
                current_len = len(para)
            else:
                current.append(para)
                current_len += len(para)

        if current:
            result.append({
                "text": "\n\n".join(current),
                "header": chunk["header"],
                "source": chunk["source"],
            })

    return result


def add_batch_with_retry(collection, ids, documents, metadatas, attempts=5):
    """Reintenta ante un 429: la cuota por minuto se recupera sola."""
    for attempt in range(attempts):
        try:
            collection.add(ids=ids, documents=documents, metadatas=metadatas)
            return
        except Exception as exc:
            quota = "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc)
            if not quota or attempt == attempts - 1:
                raise
            espera = 30 * (attempt + 1)
            print(f"    cuota agotada, reintento en {espera}s")
            time.sleep(espera)


def main():
    load_dotenv(BASE_DIR / ".env")
    if not os.environ.get("GEMINI_API_KEY", "").strip():
        raise RuntimeError("Falta GEMINI_API_KEY: los embeddings salen por la API.")
    ef = make_embedding_function()

    # ChromaDB client
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # Borrar coleccion si existe (re-indexar limpio)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"},
    )

    # Procesar todos los .md
    all_chunks = []
    for md_file in sorted(DOCS_DIR.glob("*.md")):
        print(f"Procesando {md_file.name}...")
        text = md_file.read_text(encoding="utf-8")
        source = md_file.stem
        category = CATEGORY_MAP.get(source, "rules")
        chunks = chunk_markdown(text, source)
        chunks = split_large_chunks(chunks, max_chars=1500)
        for c in chunks:
            c["category"] = category
        print(f"  {len(chunks)} chunks [{category}]")
        all_chunks.extend(chunks)

    # Indexar en ChromaDB
    total_batches = (len(all_chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"\nIndexando {len(all_chunks)} chunks en ChromaDB...")
    print(f"Son {total_batches} lotes con pausa: unos {total_batches * PAUSE_SECONDS // 60} minutos.")
    for i in range(0, len(all_chunks), BATCH_SIZE):
        batch = all_chunks[i:i + BATCH_SIZE]
        add_batch_with_retry(
            collection,
            ids=[f"chunk_{i + j}" for j in range(len(batch))],
            documents=[c["text"] for c in batch],
            metadatas=[{"header": c["header"], "source": c["source"], "category": c["category"]} for c in batch],
        )
        numero = i // BATCH_SIZE + 1
        print(f"  Lote {numero}/{total_batches}: {len(batch)} chunks indexados")
        if numero < total_batches:
            time.sleep(PAUSE_SECONDS)

    print(f"\nIngesta completa: {collection.count()} chunks en la coleccion.")


if __name__ == "__main__":
    main()
