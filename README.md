# PragyanBridge Prototype 🚀
### SIH 2026 Problem Statement 26044 • Team Echelon

**PragyanBridge** is an AI-powered candidate skill intent matching and tamper-proof NAAC accreditation platform designed for rapid evaluation during hackathon judging.

---

## 🏗️ Repository Architecture

```
pragyanbridge-prototype/
├── backend/
│   ├── main.py               # FastAPI server with lightweight SQLite DB & routes
│   ├── scoring.py            # Dynamic 70/20/10 formula calculator & AST check
│   ├── vector_engine.py      # SBERT similarity matcher (using sentence-transformers)
│   ├── seed_data.py          # Script generating 15 realistic student profiles
│   ├── requirements.txt      # fastapi, uvicorn, sentence-transformers, numpy
│   └── pragyanbridge.db      # SQLite database with pre-computed 384-dim SBERT vectors
├── frontend/
│   ├── package.json          # Next.js 14, Tailwind CSS, Lucide icons
│   └── app/
│       ├── page.tsx          # Single dashboard with Student, Recruiter & TPO views
│       ├── layout.tsx        # App layout wrapper
│       └── globals.css       # Tailwind CSS styling
├── run_demo.sh               # One-click Linux / macOS / Git Bash demo runner
├── run_demo.bat              # One-click Windows CMD / PowerShell demo runner
└── README.md                 # Project documentation & execution guide
```

---

## ⚡ Quickstart (Run Demo in 30 Seconds)

### Option 1: Using the Launcher Script
* **Windows**: Double-click `run_demo.bat` or run:
  ```cmd
  run_demo.bat
  ```
* **Linux / macOS / Git Bash**:
  ```bash
  bash run_demo.sh
  ```

### Option 2: Manual Start (Two Terminals)

**Terminal 1 — Backend (FastAPI)**:
```bash
cd backend
py seed_data.py
py -m uvicorn main:app --reload --port 8000
```
* Interactive Swagger API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

**Terminal 2 — Frontend (Next.js 14)**:
```bash
cd frontend
npm run dev
```
* Application Dashboard: [http://localhost:3000](http://localhost:3000)

---

## 🎯 3 Core Live Interactive Demo Flows

1. **Recruiter AI Intent Search & Slider Re-Ranking**:
   * Enter natural language job descriptions (e.g., *"FastAPI backend developer with SQLite, Docker, microservices"*).
   * Adjust **Assessment Test %**, **GitHub Intent %**, and **Academic CGPA %** sliders in real-time.
   * Watch candidates dynamically re-rank based on 384-dimensional SBERT cosine similarity and AST code integrity.

2. **Student GitHub Sync & Verified Skill Tree**:
   * Click **"Sync GitHub Repository"** to simulate parsing commits and running AST syntax tree integrity checks.
   * Review AST anti-cheat validated mastery badges and inspected SHA-256 digital credential ledger signatures.

3. **College TPO 1-Click NAAC Dossier Export**:
   * Click **"1-Click Download NAAC Dossier"** to export structured JSON audit evidence for:
     * **Criterion 1.3**: Curriculum Enrichment & Experiential Learning.
     * **Criterion 3.5**: Industry-Academia Collaboration & Readiness Rate.
     * **Criterion 5.2**: Student Placement & Progression.
   * Cryptographically bound with a tamper-proof SHA-256 digital signature.
