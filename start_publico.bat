@echo off
cd /d "%~dp0"
echo.
echo 1) Deja esta ventana abierta: es el chatbot.
echo 2) En otra terminal corre: cloudflared tunnel --url http://127.0.0.1:8000
echo 3) Copiá la URL https://....trycloudflare.com que imprime cloudflared.
echo.
python -m uvicorn app:app --host 127.0.0.1 --port 8000
