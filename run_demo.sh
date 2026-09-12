#!/usr/bin/env bash
# PragyanBridge Demo Launcher (SIH 2026 PS 26044 • Team Echelon)

set -e

echo "=========================================================="
echo "    Starting PragyanBridge Prototype Demo Environment     "
echo "=========================================================="

# 1. Seed the SQLite database with 15 candidate profiles & SBERT embeddings
echo "[1/3] Seeding SQLite database with 15 student profiles..."
py backend/seed_data.py || python backend/seed_data.py || python3 backend/seed_data.py

# 2. Launch FastAPI Backend Server
echo "[2/3] Launching FastAPI Backend on http://localhost:8000 ..."
py -m uvicorn main:app --reload --port 8000 --app-dir backend &
BACKEND_PID=$!

# 3. Launch Next.js Frontend
echo "[3/3] Launching Next.js Frontend on http://localhost:3000 ..."
cd frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "=========================================================="
echo "  PragyanBridge is Live!"
echo "  - Recruiter / Student / TPO Dashboard: http://localhost:3000"
echo "  - FastAPI Interactive Swagger Docs:    http://localhost:8000/docs"
echo "=========================================================="
echo "Press Ctrl+C to stop all servers."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true" EXIT INT TERM
wait
