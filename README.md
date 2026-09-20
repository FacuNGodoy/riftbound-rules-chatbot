# Riftbound Rules Chatbot

Asistente web en español que responde reglas e interacciones del TCG **Riftbound**, como un juez de mesa. Recupera el reglamento oficial (RAG), cruza el texto real de las cartas y verifica el ruling antes de mostrarlo.

Trabajo final — *Inteligencia Artificial para Programadores* (UTN FRBA).  
Autor: **Facundo Nahuel Godoy**.

## Qué hace

- Consulta de Core Rules, patch notes y legalidad de formato.
- Identificación de cartas por nombre, número (`OGN-195`) o foto (visión local con Ollama).
- Resolución de jugadas (timing, Hidden, Repeat, Deathknell, reemplazos).
- Ciclo draft → verifier: un modelo redacta, otro contrasta contra la evidencia recuperada.

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | HTML / CSS / JS (chat único) |
| Backend | Python, FastAPI |
| Memoria de reglas | ChromaDB + embeddings `gemini-embedding-001` |
| Cartas | `cards.json` (~960 cartas) |
| Juez (nube) | Gemini Flash (cadena draft + verifier) |
| Visión (local) | Ollama + `minicpm-v` |
| Publicación | Render (Web Service + Docker) |

## Cómo correrlo en local

Requisitos: Python 3.11+, [Ollama](https://ollama.com) solo si vas a adjuntar fotos de cartas, clave de [Google AI Studio](https://aistudio.google.com/apikey).

```bash
cd chatbot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

En `.env` pegá `GEMINI_API_KEY`. El índice de reglas ya viene armado en `chroma_db/`, así que alcanza con levantar el server:

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

`ingest.py` solo hace falta si cambiás los documentos de `docs/`. Tarda unos 6 minutos porque va despacio para no agotar la cuota de embeddings.

Abrí http://127.0.0.1:8000

Para visión: `ollama pull minicpm-v` y dejar Ollama corriendo.

## Publicar en Render

1. Subí este repo a GitHub (público).
2. En [render.com](https://render.com) → **New** → **Web Service** → conectá el repo.
3. Runtime: **Docker**. Plan: **Free**.
4. Environment: `GEMINI_API_KEY` (secret) y `RIFTBOUND_VISION=0`.
5. URL: `https://riftbound-rules-chatbot.onrender.com` (el nombre puede variar).

En Render **no hay fotos de cartas**. Preguntá por nombre (`Defy`) o número (`OGN-045`). El primer request después de un rato inactivo puede tardar ~1 minuto (la instancia se duerme).

## Evaluación automática

Con el server arriba:

```bash
python eval/run_eval.py --base-url http://127.0.0.1:8000
```

Los casos están en `eval/judge_cases.json`. Un log de sesión real está en `eval/sesion_real.md`.

## Seguridad

- La API key **no** va en el código: vive en `.env` (ignorado por git).
- El modelo no recibe instrucciones del usuario como system prompt: la query entra como pregunta, el reglamento entra como contexto recuperado.
- No hay cuentas de usuario: no se persisten chats ni fotos en disco.

## Estructura

```
app.py              API + orquestación (retrieval, draft, verifier)
ingest.py           Indexa docs/ en ChromaDB
docs/               Reglamento y patch notes en markdown
cards.json          Base de cartas
static/             Chat web
eval/               Casos de juez y runner
```
