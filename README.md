# PragyanBridge Prototype 🚀
### SIH 2026 Problem Statement 26044 • Team Echelon
**Portal for Academia–Industry Collaboration for Skill Mapping, Internships and Placement**

PragyanBridge bridges academic learning and industry expectations using deterministic AI matching, tamper-proof NAAC accreditation evidence, and real-time skill-gap intelligence with actionable learning roadmaps.

---

## 🏗️ Architecture & Core Invariants

```
JOB DESCRIPTION (Recruiter / Student Target Role)
      ↓
Deterministic 384-dim SBERT Vector Encoding (all-MiniLM-L6-v2)
      ↓
Deterministic 70/20/10 Composite Candidate Scoring
      ↓
Ranked Candidate Table (~20ms latency, zero LLM calls)
      ↓ (On Demand)
Canonical Skill Taxonomy & Extraction Engine (skills_engine.py)
      ↓
Deterministic Skill Gap & Coverage Analysis (% Match, Strengths, Gaps, Partial Matches)
      ↓
GenAI Explanation & Personalized 3-Step Roadmap (genai_service.py)
   ├── [Live Mode]: Google Gemini REST API via httpx (gemini-2.5-flash)
   └── [Fallback Mode]: Deterministic Algorithmic Fallback (Truthfully labeled in UI & API)
```

> [!IMPORTANT]
> **Deterministic Ranking Invariant**: SBERT vector similarity and the 70/20/10 candidate ranking rubric are strictly deterministic and mathematically reproducible. The LLM is **never** permitted to alter candidate numerical scores or rankings; it functions strictly as an explanatory and roadmap synthesis layer on demand.

---

## 📁 Repository Layout

```
pragyanbridge-prototype/
├── backend/
│   ├── main.py               # FastAPI server, endpoints, SQLite models, search & skill-gap API
│   ├── skills_engine.py      # Canonical taxonomy, alias resolution, deterministic gap & coverage %
│   ├── genai_service.py      # Prompt-injection safe Gemini REST client + intelligent fallback engine
│   ├── scoring.py            # Deterministic 70/20/10 formula calculator & Python AST analyzer
│   ├── vector_engine.py      # SBERT similarity matcher (384-dimensional dense embeddings)
│   ├── seed_data.py          # Populates SQLite DB with 15 benchmark student profiles & embeddings
│   ├── test_skill_gap.py     # 25-point comprehensive automated test suite (Unit + API Regression)
│   ├── requirements.txt      # fastapi, uvicorn, sentence-transformers, torch, httpx, pydantic
│   └── pragyanbridge.db      # SQLite database with pre-computed 384-dim SBERT vectors
├── frontend/
│   ├── package.json          # Next.js 14, React 18, Tailwind CSS, Lucide icons
│   └── app/
│       ├── page.tsx          # Single dashboard with Recruiter, Student & TPO views + Skill Gap Modal
│       ├── layout.tsx        # App layout wrapper
│       └── globals.css       # Tailwind CSS styling
├── run_demo.sh               # One-click Linux / macOS / Git Bash demo runner
├── run_demo.bat              # One-click Windows CMD / PowerShell demo runner
└── README.md                 # Project documentation & execution guide
```

---

## ⚡ Quickstart (Launch Demo in 30 Seconds)

### Option 1: One-Click Demo Runner
* **Windows**:
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
# Seed SQLite database with 15 benchmark candidates and embeddings
py backend/seed_data.py

# Start FastAPI server on port 8000
py -m uvicorn backend.main:app --reload --port 8000
```
* Interactive API Documentation (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

**Terminal 2 — Frontend (Next.js 14)**:
```bash
cd frontend
npm run dev
```
* Application Dashboard: [http://localhost:3000](http://localhost:3000)

---

## 🔑 GenAI Configuration & Fallback Guarantee

PragyanBridge includes a zero-dependency Google Gemini REST API client via `httpx`:

1. **Live GenAI Mode**:
   Set your Google Gemini API key as an environment variable before launching the backend:
   ```bash
   # Windows PowerShell
   $env:GENAI_API_KEY = "your_gemini_api_key_here"

   # Windows CMD
   set GENAI_API_KEY=your_gemini_api_key_here

   # Linux / macOS
   export GENAI_API_KEY="your_gemini_api_key_here"
   ```
   When configured, PragyanBridge calls `gemini-2.5-flash` in structured JSON mode with `temperature=0.2`. The API returns `analysis_mode: "genai"` and renders an emerald `✨ GenAI Powered (Gemini)` badge.

2. **Deterministic Fallback Mode (Offline / Unconfigured Key)**:
   If `GENAI_API_KEY` or `GEMINI_API_KEY` is not set or network fails, PragyanBridge gracefully falls back to the deterministic rule engine in `genai_service.py`. The API returns `analysis_mode: "deterministic_fallback"` and renders an amber `⚡ Deterministic Algorithmic Fallback` badge.
   * **Truthful Labeling Guarantee**: Deterministic fallbacks are **never** deceptively presented as GenAI outputs.

---

## 🎯 4 Live Interactive Demo Flows

### 1. Recruiter Intent Search, Quick JDs & Dynamic Rubric
* Select from 3 quick-fill sample JDs (*"Backend Python / FastAPI"*, *"Full Stack React & Node"*, *"Machine Learning & NLP"*) or type a custom natural language requirement.
* Adjust dynamic 70/20/10 sliders: **Assessment Test %**, **GitHub Intent %**, and **Academic CGPA %**.
* Candidates dynamically re-rank within ~20ms with deterministic `Skill Coverage %` badges displayed in real-time.

### 2. On-Demand Skill Gap Analysis & 3-Step Roadmap Modal
* In the recruiter table, click **"Analyze"** on any ranked candidate.
* An interactive modal displays:
  * SBERT Semantic Match Score vs. Deterministic Skill Coverage %
  * Active Analysis Mode (`GenAI` vs `Deterministic Fallback`)
  * **Demonstrated Strengths**: Verified skills with evidence from student codebase / assessments
  * **Target Gaps**: Missing competencies tagged with `HIGH`, `MEDIUM`, or `LOW` priority
  * **Personalized 3-Step Roadmap**: Each milestone includes duration, focus topics, and a concrete hands-on project recommendation.

### 3. Student Portal: AST Syntax Analysis & Career Readiness Roadmap
* Switch to the **Student Portal** and pick any of the 15 seeded student profiles.
* Inspect AST structural metrics and test live Python code in the interactive AST Syntax Tree Analyzer.
* Target a desired placement role (*Backend Dev*, *Full Stack Dev*, *AI/ML Engineer*, or custom) and click **"Generate Roadmap"** to get immediate career guidance.

### 4. College TPO Institutional Hub & NAAC Accreditation Export
* Switch to the **College TPO & NAAC** view.
* Inspect institutional KPIs: 15 enrolled candidates, 100% verified assessment/project evidence, canonical skill distribution across 31 skills.
* Evaluate **Benchmark Role Demand Alignment** across Senior Backend, Full Stack, ML/NLP, and Cloud DevOps.
* Click **"Download NAAC Dossier"** to generate cryptographically signed JSON audit evidence for:
  * **Criterion 1.3**: Curriculum Enrichment & Experiential Learning (100% AST analyzed projects).
  * **Criterion 3.5**: Industry-Academia Collaboration & SBERT intent vector match.
  * **Criterion 5.2**: Technical Qualification Indicators (Evaluates pre-placement technical evidence; actual employment/placement outcomes explicitly marked as "Not measured by current prototype").

---

## 🧪 Automated Verification Suite

PragyanBridge includes a 25-point automated test suite covering unit logic and full API regressions:

```bash
cd backend
py -m unittest discover -v
```

### Verified Test Groups (25 Tests):
* **Test A**: Deterministic JD skill extraction and alias resolution (`k8s` → `Kubernetes`, `postgres` → `PostgreSQL`).
* **Test B**: Candidate profile skill extraction preserving exact source provenance (`proctored_assessment`, `project_code_summary`).
* **Test C**: Deterministic skill gap computation, partial match bridges (`SQLite` ↔ `PostgreSQL`), and coverage %.
* **Test D**: Missing API key fallback (confirming `analysis_mode == "deterministic_fallback"`).
* **Test E**: Mock GenAI response with structured Pydantic schema validation.
* **Test F**: Malformed / non-JSON GenAI response handled gracefully without crashing.
* **Test G**: Prompt injection resilience against malicious instructions in untrusted JD text.
* **Test H (H1–H9)**: Full endpoint regression across all core routes (`/api/health`, `/api/candidates`, `/api/candidates/{id}`, `/api/search`, `/api/sync-github`, `/api/tpo/naac-export`, `/api/verify/{hash}`, `/api/skill-gap`).
* **Test I (I1–I4)**: Institutional intelligence hub regression (`/api/tpo/analytics`, `/api/tpo/skill-gap`, empty JD validation, enriched NAAC export).
* **Test J (J1–J5)**: Institutional coverage mathematical rigor (exact 50.0% scenario, zero-candidate handling, single required skill, duplicate/alias deduplication, and empty skill inputs).

---

## 🏆 SIH 2026 Problem Statement 26044 Alignment

| SIH Requirement | PragyanBridge Solution | Technical Mechanism |
|---|---|---|
| **Skill Mapping** | Dual-layer mapping: SBERT semantic intent + canonical skill taxonomy | 384-dim dense vectors (`all-MiniLM-L6-v2`) + deterministic alias resolution |
| **Tamper-Proof Credentials** | Immutable verification ledger & cryptographic badges | SHA-256 digital signature per student record & NAAC criteria dossier |
| **Industry Readiness** | Direct alignment between student code and recruiter JDs | 70/20/10 composite score (Assessment, Code Intent/AST, CGPA) |
| **Personalized Upskilling** | 3-step targeted placement preparation roadmap | Google Gemini REST API (`gemini-2.5-flash`) with structured JSON schema |
| **Accreditation Evidence** | Automated audit trail for NAAC SSR submission | 1-Click cryptographic dossier export for Criteria 1.3, 3.5, and 5.2 |
