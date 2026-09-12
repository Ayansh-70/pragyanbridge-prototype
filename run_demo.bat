@echo off
title PragyanBridge Demo Launcher
echo ==========================================================
echo     Starting PragyanBridge Prototype Demo Environment     
echo ==========================================================

echo [1/3] Seeding SQLite database with 15 candidate profiles...
py backend\seed_data.py

echo [2/3] Launching FastAPI Backend on http://localhost:8000 ...
start "PragyanBridge Backend (FastAPI)" cmd /k "py -m uvicorn main:app --reload --port 8000 --app-dir backend"

echo [3/3] Launching Next.js Frontend on http://localhost:3000 ...
start "PragyanBridge Frontend (Next.js)" cmd /k "cd frontend && npm run dev"

echo.
echo ==========================================================
echo  PragyanBridge is Live!
echo  - Recruiter / Student / TPO Dashboard: http://localhost:3000
echo  - FastAPI Interactive Swagger Docs:    http://localhost:8000/docs
echo ==========================================================
pause
