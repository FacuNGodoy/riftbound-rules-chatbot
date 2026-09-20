@echo off
cd /d "%~dp0"
echo Riftbound Rules Chatbot — http://127.0.0.1:8000
python -m uvicorn app:app --host 127.0.0.1 --port 8000
