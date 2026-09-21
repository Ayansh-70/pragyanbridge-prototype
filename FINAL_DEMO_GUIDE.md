# PragyanBridge — Final SIH 2026 Live Demo & Presentation Guide 🚀
### Problem Statement: SIH 2026 — PS 26044 • Team ECHELON
**"Portal for Academia–Industry Collaboration for Skill Mapping, Internships and Placement"**

---

## 📋 Table of Contents
1. [Executive Summary & Setup](#1-executive-summary--setup)
2. [Demo Environment & Credentials](#2-demo-environment--credentials)
3. [Selected Benchmark Demo Profile (Aditya Sharma)](#3-selected-benchmark-demo-profile-aditya-sharma)
4. [Selected Benchmark Job Description](#4-selected-benchmark-job-description)
5. [Tight 3–5 Minute 4-Pillar Demo Flow](#5-tight-35-minute-4-pillar-demo-flow)
6. [Step-by-Step UI Clicks & Spoken Script](#6-step-by-step-ui-clicks--spoken-script)
7. [GenAI Mode vs. Deterministic Fallback Verification](#7-genai-mode-vs-deterministic-fallback-verification)
8. [Defensible Terminology & Honest Limitations](#8-defensible-terminology--honest-limitations)
9. [Judge Q&A Cheat Sheet (Top 10 High-Frequency Questions)](#9-judge-qa-cheat-sheet-top-10-high-frequency-questions)

---

## 1. Executive Summary & Setup

PragyanBridge bridges academic learning and industry expectations using deterministic AI matching, tamper-proof NAAC accreditation evidence, and real-time skill-gap intelligence with actionable learning roadmaps.

### 🚀 One-Click Launch
* **Windows (CMD / PowerShell)**:
  ```cmd
  run_demo.bat
  ```
* **Linux / macOS / Git Bash**:
  ```bash
  bash run_demo.sh
  ```

### 🛠️ Manual Launch (Two Terminals)

**Terminal 1 — Backend (FastAPI)**:
```bash
# Seed SQLite database (15 benchmark candidates + embeddings)
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
* Web Dashboard: [http://localhost:3000](http://localhost:3000)

---

## 2. Demo Environment & Credentials

| Component | Specification | Port / Endpoint |
|---|---|---|
| **Frontend** | Next.js 14 (React 18, Tailwind CSS, Lucide Icons) | `http://localhost:3000` |
| **Backend API** | FastAPI (Python 3.10+ / 3.14 compatible) | `http://localhost:8000` |
| **Vector Engine** | SBERT `sentence-transformers/all-MiniLM-L6-v2` (384-dim) | In-Memory PyTorch / CPU (~20ms latency) |
| **Database** | SQLite (`backend/pragyanbridge.db`) | 15 Candidates, 15 Projects, 15 Scores |
| **GenAI Model** | Google Gemini REST API (`gemini-2.5-flash`) via `httpx` | Structured JSON output (`temperature=0.2`) |
| **Fallback Engine** | Algorithmic Rule Engine (`genai_service.py`) | Offline / zero-cost fallback mode |

---

## 3. Selected Benchmark Demo Profile (Aditya Sharma)

Always use **Aditya Sharma (`cand-01`)** as the primary demonstration candidate. His records are pre-seeded and fully verified across assessments, projects, AST traversals, and cryptographic ledger signatures.

* **Candidate ID**: `cand-01`
* **Student Name**: Aditya Sharma
* **College ID**: `PIT-CSE-22-041`
* **Academic CGPA**: `9.12` / 10.0
* **GitHub Handle**: `aditya-fastapi`
* **Proctored Assessment**: `FastAPI & Microservices` — Score: **94.5%**
* **Project Title**: `High-Throughput Asynchronous Task Pipeline`
* **Project Commits**: `42`
* **AST Structural Complexity Score**: **70.2%** (Deterministic syntax tree traversal)
* **Cryptographic SHA-256 Ledger Hash**:
  ```
  0a7c7d3d344427b358b5127ac0909ffc512e737235079cbcedc8f9377ee64b3a
  ```
* **Payload Format**: `PRAGYANBRIDGE:cand-01:Aditya Sharma:PIT-CSE-22-041:9.12:TAMPER_PROOF_SECURE`

---

## 4. Selected Benchmark Job Description

Use this exact benchmark JD during the live presentation. It triggers a crisp, realistic skill gap without any noise:

```text
FastAPI backend developer with SQLite, microservices and REST API skills, Docker containerization, and Redis caching.
```

### Expected Evaluation Breakdown:
* **Extracted Target Role**: Backend Developer
* **Extracted Required Skills (6)**: `FastAPI`, `Microservices`, `SQLite`, `REST APIs`, `Docker`, `Redis`
* **Candidate Matched Strengths (4)**: `FastAPI`, `Microservices`, `Redis`, `SQLite`
* **Candidate Skill Gaps (2)**:
  * `Docker` (Priority: **HIGH** — Containerization missing from project code)
  * `REST APIs` (Priority: **MEDIUM** — Core API design conventions)
* **Skill Coverage Ratio**: **66.7%** (4 / 6 skills matched)
* **Ranked Position**: **#1** among 15 candidates under default 70/20/10 weights

---

## 5. Tight 3–5 Minute 4-Pillar Demo Flow

```
[0:00 - 0:45] PILLAR 1: SMART RECRUITER MATCHING & DYNAMIC RUBRIC
               Paste JD → Instant SBERT Vector Matching → Adjust 70/20/10 Sliders → Candidate #1 Rank
      ↓
[0:45 - 2:00] PILLAR 2: ON-DEMAND SKILL GAP ANALYSIS & 3-STEP ROADMAP
               Click "Analyze" on Aditya Sharma → Compare SBERT vs Skill Coverage % →
               View Strengths & Missing Gaps → Review GenAI 3-Step Milestone Roadmap
      ↓
[2:00 - 3:15] PILLAR 3: STUDENT PORTAL & AST CODE VERIFICATION
               Switch to Student View → Select Aditya Sharma → Inspect AST Code Metrics →
               Demonstrate SHA-256 Tamper-Proof Digital Badge & Verification Ledger
      ↓
[3:15 - 4:15] PILLAR 4: INSTITUTIONAL HUB & NAAC ACCREDITATION EXPORT
               Switch to TPO / NAAC View → Institutional Skill Coverage & Benchmark Role Demand →
               1-Click "Download NAAC Dossier" (Criteria 1.3, 3.5, 5.2 pre-placement indicators)
      ↓
[4:15 - 5:00] WRAP-UP & JUDGE Q&A
               Highlight Deterministic Core + GenAI Advisory Layer + Truth in Accreditation
```

---

## 6. Step-by-Step UI Clicks & Spoken Script

### Pillar 1: Recruiter Matching & Explainable Rubric (0:00 – 0:45)
1. **Navigate**: Open `http://localhost:3000`. Ensure the top navigation is set to **"Recruiter Portal"**.
2. **Action**: Click the quick button **"Backend Python / FastAPI"** or paste:
   `FastAPI backend developer with SQLite, microservices and REST API skills, Docker containerization, and Redis caching.`
3. **Action**: Click **"Run Match"** (or press Enter).
4. **Spoken Narration**:
   > *"Judges, current hiring relies on keyword-stuffed resumes that produce high screening drop-offs. PragyanBridge replaces resume claims with verified technical evidence. When a recruiter inputs a natural language JD, our local SBERT vector engine matches semantic intent against student codebases and assessments in 20 milliseconds without making any external API calls. Candidates are ranked using a transparent 70/20/10 rubric: 70% proctored assessment, 20% project code structural evidence, and 10% academic CGPA. Here, Aditya Sharma ranks #1 with a 66.7% skill coverage score."*
5. **Action**: Drag the **GitHub Project %** slider up to 40% and **Assessment %** to 50%. Point out that the candidate scores dynamically recalculate client-side in real-time.

### Pillar 2: Candidate Skill Gap & 3-Step Roadmap Modal (0:45 – 2:00)
1. **Action**: On Aditya Sharma's row (`cand-01`), click the indigo **"Analyze"** button.
2. **Modal Opens**: Point to the two KPI metric cards at the top:
   - Semantic Vector Match: **~88%**
   - Deterministic Skill Coverage: **66.7%**
3. **Point out the badge**:
   - If `GENAI_API_KEY` is configured: Emerald badge `✨ GenAI Powered (Gemini)`.
   - If offline or key absent: Amber badge `⚡ Deterministic Algorithmic Fallback`.
4. **Action**: Scroll to **"Demonstrated Strengths"** (`FastAPI`, `Microservices`, `Redis`, `SQLite`) with source provenance tags (`Assessment`, `Project Code`).
5. **Action**: Scroll to **"Target Skill Gaps"** (`Docker` - HIGH priority, `REST APIs` - MEDIUM priority).
6. **Action**: Review the **"Personalized 3-Step Upskilling Roadmap"**:
   - Step 1: Docker Containerization Fundamentals (Week 1–2)
   - Step 2: RESTful API Contract Design & OpenAPI Specification (Week 3)
   - Step 3: End-to-End Containerized Microservices Capstone Project (Week 4)
7. **Spoken Narration**:
   > *"Notice our core architectural invariant: the LLM is never allowed to invent or alter candidate scores. Our deterministic rule engine establishes the mathematical skill gap first. Gemini or our offline fallback engine is then called strictly on demand to formulate an actionable 3-step learning pathway with specific project deliverables, closing the exact delta between candidate capability and employer needs."*
8. **Action**: Close the modal (click `X` or "Close").

### Pillar 3: Student Diagnostic Radar & AST Verification (2:00 – 3:15)
1. **Navigate**: Click **"Student Portal"** in the top navigation bar.
2. **Action**: Select **"Aditya Sharma (cand-01)"** from the candidate selector dropdown.
3. **Inspect Radar & Projects**:
   - Point out the Diagnostic Skill Radar showing verified skill scores.
   - Point out project `High-Throughput Asynchronous Task Pipeline`, 42 commits, AST Score: `70.2%`.
4. **Action**: Scroll to **"Interactive AST Syntax Tree Analyzer"**. Click **"Analyze Code Structure"** with sample Python code.
5. **Action**: Point out the SHA-256 Digital Badge at the bottom of the student card:
   - Hash: `0a7c7d3d3444...`
   - Issuer: `PragyanBridge NAAC Verifiable Credential Service`
6. **Spoken Narration**:
   > *"In the Student Portal, students receive continuous diagnostic feedback rather than guessing what industry wants. Our Python AST engine parses the Abstract Syntax Tree of the student's project code to measure structural complexity, modularity, and control-flow density. We want to be completely honest with the jury: AST parsing proves syntactic validity and structural modularity—it does not claim to detect plagiarism or verify original authorship. Furthermore, every candidate's credential is cryptographically hashed with SHA-256 to ensure local ledger record integrity."*

### Pillar 4: Institutional Hub & NAAC Accreditation Export (3:15 – 4:15)
1. **Navigate**: Click **"College TPO & NAAC"** in the top navigation bar.
2. **Inspect Institutional KPIs**:
   - Enrolled Candidates: **15**
   - Verified Evidence Rate: **100%**
   - Tracked Skills: **31 canonical technologies**
3. **Action**: Scroll to **"Benchmark Role Demand Alignment"**. Show the institutional skill coverage across roles:
   - Senior Backend Developer: **46.7%** institutional coverage
   - Machine Learning & NLP Engineer: **33.3%** institutional coverage
   - Full Stack Web Developer: **40.0%** institutional coverage
4. **Action**: Click the purple **"Download NAAC Dossier"** button.
5. **Inspect Exported Payload**: Show that a cryptographic JSON dossier is downloaded containing structured evidence for:
   - **Criterion 1.3**: Curriculum Enrichment & Experiential Learning (100% verified AST project evidence)
   - **Criterion 3.5**: Industry-Academia Linkages (Semantic matching vector alignment)
   - **Criterion 5.2**: Technical Qualification Indicators (Pre-placement technical evidence; explicitly notes that post-offer employment outcomes are not measured by the prototype).
6. **Spoken Narration**:
   > *"Finally, the Institutional TPO Hub solves the primary administrative bottleneck for universities: accreditation evidence. Instead of manual data collection across spreadsheets, PragyanBridge continuously aggregates cohort skill coverage against industry demand. With one click, the TPO exports an audit-ready dossier mapped directly to NAAC SSR Criteria 1.3, 3.5, and 5.2, backed by cryptographic ledger timestamps."*

### Wrap-Up (4:15 – 5:00)
> *"In summary: PragyanBridge delivers deterministic AI matching for recruiters, actionable gap roadmaps for students, and auditable NAAC evidence for institutions—with zero black-box scoring and 100% uptime reliability."*

---

## 7. GenAI Mode vs. Deterministic Fallback Verification

PragyanBridge guarantees uninterrupted presentations regardless of internet connectivity or API quota limits:

| State | Environmental Condition | UI Visual Indicator | API Payload Field |
|---|---|---|---|
| **Live GenAI Mode** | `GENAI_API_KEY` set & active | Emerald Badge: `✨ GenAI Powered (Gemini)` | `"analysis_mode": "genai"` |
| **Deterministic Fallback** | Key unset, quota exceeded, or offline | Amber Badge: `⚡ Deterministic Algorithmic Fallback` | `"analysis_mode": "deterministic_fallback"` |

### How to Toggle Between Modes During Practice:
* **To force Fallback Mode**: Launch backend without `GENAI_API_KEY` (or set it to `""`).
* **To enable Live Gemini Mode**:
  ```bash
  export GENAI_API_KEY="AIzaSy..."
  py -m uvicorn backend.main:app --reload --port 8000
  ```

---

## 8. Defensible Terminology & Honest Limitations

Judges respect engineering honesty over inflated marketing claims. Always use these exact disclosures:

| Feature Area | What It PROVES (Defensible Claim) | What It DOES NOT PROVE (Do Not Claim) |
|---|---|---|
| **Python AST Analysis** | Valid syntax parsing, structural modularity, function/class node counts, control flow complexity. | Does **NOT** prove human authorship, identity, or detect advanced external plagiarism. |
| **SHA-256 Ledger Hash** | Cryptographic record integrity (ensures student CGPA, ID, and test scores have not been tampered with in the database). | Does **NOT** prove external physical university degree issuance or physical exam proctoring. |
| **NAAC Criterion 5.2** | Pre-placement technical evidence readiness indicators (assessment scores, project complexity, CGPA). | Does **NOT** measure actual post-college employment outcomes or salary packages. |
| **SBERT Matching** | Mathematical cosine similarity between 384-dimensional dense semantic vectors of JD and candidate code. | Does **NOT** perform subjective human interviewing or cultural fit evaluation. |
| **Gemini Roadmap** | Context-aware pedagogical milestone synthesis based strictly on calculated missing skills. | Does **NOT** alter, compute, or override numerical candidate rankings or coverage percentages. |

---

## 9. Judge Q&A Cheat Sheet (Top 10 High-Frequency Questions)

### Q1: "Why not just use LinkedIn or Naukri?"
> **Answer**: *"LinkedIn and Naukri are resume-based advertising boards that rely entirely on self-reported, unverified claims. Recruiters spend days filtering keyword-stuffed resumes. PragyanBridge is an evidence-first matching platform: candidates are ranked by proctored assessment scores, AST-verified project code, and institutional CGPA. Furthermore, LinkedIn provides zero institutional reporting for NAAC SSR accreditation."*

### Q2: "What part of this system is actually AI vs. deterministic code?"
> **Answer**: *"We deliberately split AI into two bounded layers:
> 1. **Semantic Vector Search**: SBERT (`all-MiniLM-L6-v2`) generates 384-dimensional dense embeddings to match JD intent with student project summaries.
> 2. **Pedagogical GenAI Layer**: Google Gemini (`gemini-2.5-flash`) generates personalized 3-step learning roadmaps.
> 3. **Everything else is 100% deterministic**: Skill extraction, gap computation, coverage percentages, and the 70/20/10 ranking rubric are pure deterministic mathematics. This prevents AI hallucinations from deciding student career rankings."*

### Q3: "Can a student cheat your AST code score by copy-pasting dummy loops?"
> **Answer**: *"AST analysis evaluates structural modularity, function counts, and cyclomatic complexity. While a student could artificially introduce boilerplate syntax, the AST score accounts for only 20% of the composite score. 70% is anchored by proctored skill assessments, and 10% by university CGPA. In our production roadmap, AST analysis will be paired with AST-diff similarity matching across peer submissions to detect structural plagiarism."*

### Q4: "Why are you using SQLite instead of PostgreSQL in this demo?"
> **Answer**: *"For this hackathon prototype, SQLite provides zero-dependency, self-contained, portable execution with sub-5ms query latency across our 15 benchmark candidates. In our documented Phase 2 production architecture, we migrate to PostgreSQL with `pgvector` for scalable horizontal vector indexing."*

### Q5: "What happens if Gemini is offline or rate-limited during a live deployment?"
> **Answer**: *"PragyanBridge has zero hard dependencies on external LLM availability. If Gemini is unreachable or unconfigured, our deterministic fallback engine immediately synthesizes rule-based roadmaps mapped to our canonical skill taxonomy. The UI transparently displays the amber fallback badge, ensuring 100% service availability."*

### Q6: "How do you prevent Prompt Injection attacks in the Job Description?"
> **Answer**: *"We employ a 3-tier defense: First, the Job Description is never directly concatenated into an LLM prompt for ranking—ranking is performed by local SBERT embeddings. Second, our canonical skill engine deterministically parses and whitelists skills before any LLM call. Third, the GenAI prompt strictly encapsulates the JD in XML delimiters with explicit instructions to ignore prompt overrides, and responses are enforced against a strict Pydantic JSON schema."*

### Q7: "How does the 70/20/10 weighting formula work?"
> **Answer**: *"The composite score is calculated as:
> $$\text{Score} = (0.70 \times \text{Assessment Score}) + (0.20 \times \text{AST Project Score}) + (0.10 \times \text{Normalized CGPA})$$
> In the Recruiter Portal, recruiters have dynamic sliders allowing them to adjust these weights to fit their hiring criteria, with candidates re-ranking client-side in real time."*

### Q8: "How does this align with NAAC Criteria?"
> **Answer**: *"Universities spend months compiling evidence for NAAC SSR. PragyanBridge provides direct cryptographic evidence for:
> * **Criterion 1.3**: Curriculum Enrichment & student project-based learning.
> * **Criterion 3.5**: Industry linkages through real-time demand matching.
> * **Criterion 5.2**: Student progression and technical qualification readiness indicators."*

### Q9: "How long does a search request take?"
> **Answer**: *"Once the local SBERT model weights are loaded into CPU memory, an intent search across candidates takes approximately 20 to 40 milliseconds. Skill gap extraction and deterministic coverage analysis execute in under 15 milliseconds."*

### Q10: "What is your roadmap for production deployment?"
> **Answer**: *"Our Phase 2 post-hackathon roadmap includes:
> 1. Migrating to PostgreSQL with `pgvector` for 100,000+ candidate vector indexing.
> 2. Integration with DigiLocker and National Academic Depository (NAD) for external degree verification.
> 3. University LMS integration (Moodle / Canvas) to auto-ingest lab assessments.
> 4. Role-based OAuth2 / SSO authentication for students, faculty, and recruiters."*
