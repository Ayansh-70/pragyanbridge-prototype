import os
import sys
import json
import sqlite3
import logging

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(__file__))

from main import get_db_connection, init_db
from vector_engine import generate_embedding

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pragyanbridge.seed")

STUDENTS_DATA = [
    {
        "id": "cand-01",
        "name": "Aditya Sharma",
        "college_id": "PIT-CSE-22-041",
        "cgpa": 9.12,
        "github_handle": "aditya-fastapi",
        "project": {
            "id": "proj-01",
            "title": "High-Throughput Asynchronous Task Pipeline",
            "description": "Distributed task worker pool using FastAPI, Redis queue, and SQLite state persistence.",
            "code_summary": "Asynchronous REST API service built with FastAPI, SQLite, Pydantic v2 schemas, Redis background job dispatching, and Docker containerization.",
            "commit_count": 42,
            "ast_integrity_score": 98.4
        },
        "score": {
            "id": "score-01",
            "skill": "FastAPI & Microservices",
            "test_score": 94.5
        }
    },
    {
        "id": "cand-02",
        "name": "Pooja Hegde",
        "college_id": "PIT-AI-22-019",
        "cgpa": 8.85,
        "github_handle": "pooja-genai",
        "project": {
            "id": "proj-02",
            "title": "Contextual Document Intent Semantic Matcher",
            "description": "Natural language query understanding using SentenceTransformers SBERT 384-dimensional embeddings.",
            "code_summary": "PyTorch and HuggingFace SBERT semantic vector search engine, cosine similarity matrix operations, tokenization, and dynamic re-ranking.",
            "commit_count": 35,
            "ast_integrity_score": 96.2
        },
        "score": {
            "id": "score-02",
            "skill": "PyTorch & SBERT NLP",
            "test_score": 91.0
        }
    },
    {
        "id": "cand-03",
        "name": "Rohan Varma",
        "college_id": "PIT-CSE-22-088",
        "cgpa": 8.45,
        "github_handle": "rohan-react",
        "project": {
            "id": "proj-03",
            "title": "Modern Reactive Analytics Dashboard",
            "description": "Production Next.js 14 web application featuring client state management and Tailwind CSS.",
            "code_summary": "Next.js 14 App Router, React 18, Tailwind CSS, Lucide icons, responsive dashboard views, dynamic state hooks, and client-side caching.",
            "commit_count": 28,
            "ast_integrity_score": 95.8
        },
        "score": {
            "id": "score-03",
            "skill": "Next.js & Frontend Architecture",
            "test_score": 87.0
        }
    },
    {
        "id": "cand-04",
        "name": "Sneha Mukherjee",
        "college_id": "PIT-IT-22-014",
        "cgpa": 9.30,
        "github_handle": "sneha-devops",
        "project": {
            "id": "proj-04",
            "title": "Automated Multi-Cluster Kubernetes Deployment",
            "description": "GitOps CI/CD delivery pipeline for microservices using Helm charts and Docker.",
            "code_summary": "Cloud infrastructure automation with Kubernetes, Docker container multi-stage builds, Helm charts, GitHub Actions workflows, and Prometheus metrics.",
            "commit_count": 39,
            "ast_integrity_score": 97.5
        },
        "score": {
            "id": "score-04",
            "skill": "Kubernetes & DevOps",
            "test_score": 88.5
        }
    },
    {
        "id": "cand-05",
        "name": "Karthik Iyer",
        "college_id": "PIT-CSE-22-052",
        "cgpa": 8.92,
        "github_handle": "karthik-go",
        "project": {
            "id": "proj-05",
            "title": "Sub-Millisecond gRPC Event Streamer",
            "description": "High-concurrency messaging service in Go with protocol buffers and PostgreSQL storage.",
            "code_summary": "Golang microservice communicating over gRPC, goroutine worker pools, channels, SQL connection pooling with PostgreSQL, and low latency benchmarks.",
            "commit_count": 48,
            "ast_integrity_score": 99.1
        },
        "score": {
            "id": "score-05",
            "skill": "Go & Distributed Systems",
            "test_score": 93.0
        }
    },
    {
        "id": "cand-06",
        "name": "Ananya Rao",
        "college_id": "PIT-DS-22-007",
        "cgpa": 8.78,
        "github_handle": "ananya-data",
        "project": {
            "id": "proj-06",
            "title": "Distributed Stream Processing with Spark",
            "description": "Real-time ETL data pipeline handling telemetry ingestion and anomaly classification.",
            "code_summary": "Python and PySpark streaming pipeline, Scikit-learn random forest classifier, Parquet columnar data formatting, and automated validation.",
            "commit_count": 31,
            "ast_integrity_score": 95.0
        },
        "score": {
            "id": "score-06",
            "skill": "Data Engineering & Spark",
            "test_score": 86.5
        }
    },
    {
        "id": "cand-07",
        "name": "Vikram Malhotra",
        "college_id": "PIT-CSE-22-105",
        "cgpa": 8.60,
        "github_handle": "vikram-fullstack",
        "project": {
            "id": "proj-07",
            "title": "Collaborative Realtime Workspace",
            "description": "Full-stack web application with FastAPI, WebSockets, React UI, and SQLite persistence.",
            "code_summary": "Full-stack development with FastAPI backend, WebSocket bidirectional messaging, React single page application, JWT authentication, and SQLite transactions.",
            "commit_count": 34,
            "ast_integrity_score": 96.5
        },
        "score": {
            "id": "score-07",
            "skill": "Fullstack Web & WebSockets",
            "test_score": 89.0
        }
    },
    {
        "id": "cand-08",
        "name": "Divya Patel",
        "college_id": "PIT-IT-22-033",
        "cgpa": 8.95,
        "github_handle": "divya-ui",
        "project": {
            "id": "proj-08",
            "title": "Accessible Design System Component Kit",
            "description": "Enterprise-grade React component library adhering to WCAG 2.1 AAA accessibility.",
            "code_summary": "Modular React components, Tailwind CSS utility styling, TypeScript strict typing, Storybook documentation, and comprehensive automated UI unit tests.",
            "commit_count": 26,
            "ast_integrity_score": 97.0
        },
        "score": {
            "id": "score-08",
            "skill": "React & UI/UX Systems",
            "test_score": 90.5
        }
    },
    {
        "id": "cand-09",
        "name": "Siddharth Joshi",
        "college_id": "PIT-CSE-22-012",
        "cgpa": 9.05,
        "github_handle": "sid-crypto",
        "project": {
            "id": "proj-09",
            "title": "Tamper-Proof Credential Verification Service",
            "description": "Cryptographic SHA-256 digital badging ledger with QR validation endpoints.",
            "code_summary": "Python cryptographic verification backend with SHA-256 digital signatures, Merkel tree verification, HMAC validation, and automated auditing endpoints.",
            "commit_count": 44,
            "ast_integrity_score": 98.9
        },
        "score": {
            "id": "score-09",
            "skill": "Applied Cryptography & Security",
            "test_score": 95.0
        }
    },
    {
        "id": "cand-10",
        "name": "Meera Krishnan",
        "college_id": "PIT-AI-22-044",
        "cgpa": 8.70,
        "github_handle": "meera-vision",
        "project": {
            "id": "proj-10",
            "title": "Realtime Video Edge Detection System",
            "description": "Computer vision pipeline executing YOLOv8 model inference on compressed video streams.",
            "code_summary": "PyTorch and OpenCV computer vision application, convolutional neural networks, object bounding box tracking, and ONNX runtime optimization.",
            "commit_count": 30,
            "ast_integrity_score": 94.8
        },
        "score": {
            "id": "score-10",
            "skill": "Computer Vision & PyTorch",
            "test_score": 85.0
        }
    },
    {
        "id": "cand-11",
        "name": "Tanmay Deshmukh",
        "college_id": "PIT-CSE-22-076",
        "cgpa": 9.25,
        "github_handle": "tanmay-systems",
        "project": {
            "id": "proj-11",
            "title": "Safe Async File Storage Engine",
            "description": "High performance concurrent key-value store using memory-mapped I/O and ACID safeguards.",
            "code_summary": "Low-level systems programming in Rust and C++, zero-cost abstractions, async Tokio runtime, lock-free data structures, and POSIX filesystem hooks.",
            "commit_count": 51,
            "ast_integrity_score": 99.2
        },
        "score": {
            "id": "score-11",
            "skill": "Systems Programming & Rust",
            "test_score": 96.0
        }
    },
    {
        "id": "cand-12",
        "name": "Neha Sundaram",
        "college_id": "PIT-IT-22-089",
        "cgpa": 8.55,
        "github_handle": "neha-web",
        "project": {
            "id": "proj-12",
            "title": "Offline-First Progressive Web App",
            "description": "Client-side offline sync with Service Workers, IndexedDB, and Next.js frontend.",
            "code_summary": "Progressive Web App development with Next.js, TypeScript, Service Worker caching strategies, IndexedDB local persistence, and background synchronization.",
            "commit_count": 27,
            "ast_integrity_score": 95.4
        },
        "score": {
            "id": "score-12",
            "skill": "Next.js & Offline Web",
            "test_score": 84.0
        }
    },
    {
        "id": "cand-13",
        "name": "Rahul Nair",
        "college_id": "PIT-AI-22-061",
        "cgpa": 8.90,
        "github_handle": "rahul-llm",
        "project": {
            "id": "proj-13",
            "title": "Retrieval Augmented QA Bot with SBERT",
            "description": "RAG pipeline answering technical questions from Markdown code repositories using vector search.",
            "code_summary": "SBERT SentenceTransformers embedding extraction, LangChain document chunking, FAISS vector indexing, and contextual query ranking.",
            "commit_count": 37,
            "ast_integrity_score": 97.1
        },
        "score": {
            "id": "score-13",
            "skill": "LLM Agents & RAG",
            "test_score": 92.5
        }
    },
    {
        "id": "cand-14",
        "name": "Ishita Sen",
        "college_id": "PIT-CSE-22-029",
        "cgpa": 8.35,
        "github_handle": "ishita-cloud",
        "project": {
            "id": "proj-14",
            "title": "Serverless Event Notification Microservice",
            "description": "Event-driven asynchronous messaging broker built on Node.js and Redis Pub/Sub.",
            "code_summary": "Node.js asynchronous event architecture, Express REST API, Redis publish-subscribe messaging, Docker containerization, and automated integration tests.",
            "commit_count": 25,
            "ast_integrity_score": 94.5
        },
        "score": {
            "id": "score-14",
            "skill": "Node.js & Cloud Functions",
            "test_score": 83.0
        }
    },
    {
        "id": "cand-15",
        "name": "Abhinav Gupta",
        "college_id": "PIT-IT-22-058",
        "cgpa": 8.65,
        "github_handle": "abhinav-django",
        "project": {
            "id": "proj-15",
            "title": "Scalable Multi-Tenant REST API Platform",
            "description": "Enterprise web backend with Django REST Framework, Celery task queues, and PostgreSQL.",
            "code_summary": "Django REST Framework, relational database schema design, Celery background worker orchestration, Redis cache layer, and automated API documentation.",
            "commit_count": 33,
            "ast_integrity_score": 96.0
        },
        "score": {
            "id": "score-15",
            "skill": "Django & Database Systems",
            "test_score": 88.0
        }
    }
]

def seed():
    """Populates SQLite database with 15 realistic student profiles and SBERT embeddings."""
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    logger.info("Purging existing records for fresh demo seed...")
    cursor.execute("DELETE FROM scores;")
    cursor.execute("DELETE FROM projects;")
    cursor.execute("DELETE FROM candidates;")

    logger.info(f"Generating SBERT embeddings and inserting {len(STUDENTS_DATA)} student profiles...")

    for student in STUDENTS_DATA:
        # Insert Candidate
        cursor.execute("""
            INSERT INTO candidates (id, name, college_id, cgpa, github_handle)
            VALUES (?, ?, ?, ?, ?)
        """, (
            student["id"],
            student["name"],
            student["college_id"],
            student["cgpa"],
            student["github_handle"]
        ))

        # Generate SBERT 384-dim embedding for code summary
        proj = student["project"]
        logger.info(f"  -> Generating SBERT embedding for {student['name']}: {proj['title']}")
        embedding_vector = generate_embedding(proj["code_summary"])
        embedding_json = json.dumps(embedding_vector)

        # Insert Project
        cursor.execute("""
            INSERT INTO projects (id, candidate_id, title, description, code_summary, commit_count, ast_integrity_score, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            proj["id"],
            student["id"],
            proj["title"],
            proj["description"],
            proj["code_summary"],
            proj["commit_count"],
            proj["ast_integrity_score"],
            embedding_json
        ))

        # Insert Score
        score = student["score"]
        cursor.execute("""
            INSERT INTO scores (id, candidate_id, skill, test_score)
            VALUES (?, ?, ?, ?)
        """, (
            score["id"],
            student["id"],
            score["skill"],
            score["test_score"]
        ))

    conn.commit()
    conn.close()
    logger.info("Successfully seeded 15 candidate records with live SBERT embeddings!")

if __name__ == "__main__":
    seed()
