FROM python:3.11-slim-bookworm

# El plan gratuito de Render tiene 512 MB: la imagen no carga modelos locales.
# El índice de reglas viene construido (ingest.py se corre en desarrollo) y los
# embeddings de las preguntas salen por la API de Gemini.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    RIFTBOUND_VISION=0 \
    ANONYMIZED_TELEMETRY=False \
    MALLOC_ARENA_MAX=2

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py embeddings.py cards.json start.sh ./
COPY static/ static/
COPY chroma_db/ chroma_db/

RUN chmod +x start.sh

EXPOSE 8000
CMD ["./start.sh"]
