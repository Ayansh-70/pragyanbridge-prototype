import os
import json
import logging
from typing import List, Dict, Any, Optional
import numpy as np

# Suppress HuggingFace hub warnings for clean demo logs
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

logger = logging.getLogger("pragyanbridge.vector_engine")

# Lazy-loaded model instance
_model = None

def get_sbert_model():
    """Lazily loads and returns the SentenceTransformer model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading SentenceTransformer('all-MiniLM-L6-v2')...")
            _model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("SentenceTransformer model loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer directly: {e}. Using deterministic fallback vectorizer.")
            _model = FallbackVectorizer()
    return _model

class FallbackVectorizer:
    """Fast, deterministic fallback vectorizer (384-dim) for lightweight demo environments."""
    def __init__(self, dim: int = 384):
        self.dim = dim

    def encode(self, texts, convert_to_numpy: bool = True):
        is_single = isinstance(texts, str)
        if is_single:
            texts = [texts]

        vectors = []
        for text in texts:
            vec = np.zeros(self.dim, dtype=np.float32)
            words = text.lower().split()
            if not words:
                vectors.append(vec)
                continue
            for i, word in enumerate(words):
                h = hash(word) % self.dim
                vec[h] += 1.0 / (i + 1) ** 0.5
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            vectors.append(vec)

        res = np.array(vectors, dtype=np.float32)
        return res[0] if is_single else res

def generate_embedding(text: str) -> List[float]:
    """Generates a 384-dimensional embedding vector for a given text."""
    model = get_sbert_model()
    emb = model.encode(text)
    if hasattr(emb, "tolist"):
        return emb.tolist()
    return list(emb)

def compute_cosine_similarity(vec_a: Any, vec_b: Any) -> float:
    """Calculates cosine similarity between two numeric vectors."""
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    dot = np.dot(a, b)
    similarity = float(dot / (norm_a * norm_b))
    # Bound between 0.0 and 1.0 for ranking purposes
    return max(0.0, min(1.0, similarity))

def semantic_search(
    jd_text: str,
    candidates_list: List[Dict[str, Any]],
    w_test: float = 0.7,
    w_git: float = 0.2,
    w_acad: float = 0.1
) -> List[Dict[str, Any]]:
    """
    Performs SBERT semantic similarity matching of candidate projects against JD text
    and applies the dynamic 70/20/10 scoring rubric.

    Formula:
    Composite Score = (TestScore * w_test) + (GitScore * w_git) + (CGPA_Normalized * w_acad)
    """
    if not candidates_list:
        return []

    # Normalize weights so they sum to 1.0 if not already
    total_w = w_test + w_git + w_acad
    if total_w > 0:
        norm_w_test = w_test / total_w
        norm_w_git = w_git / total_w
        norm_w_acad = w_acad / total_w
    else:
        norm_w_test, norm_w_git, norm_w_acad = 0.7, 0.2, 0.1

    # 1. Generate SBERT vector for the Job Description (JD) text
    model = get_sbert_model()
    jd_vector = model.encode(jd_text)

    ranked_results = []

    for cand in candidates_list:
        # Resolve candidate project embedding
        cand_emb = cand.get("embedding")
        if isinstance(cand_emb, str):
            try:
                cand_emb = json.loads(cand_emb)
            except Exception:
                cand_emb = None

        # If embedding wasn't pre-computed, compute from project summary or description
        if cand_emb is None or len(cand_emb) == 0:
            summary_text = (
                cand.get("code_summary")
                or cand.get("description")
                or cand.get("title")
                or cand.get("name", "")
            )
            cand_emb = model.encode(summary_text)

        # 2. Calculate cosine similarity score against candidate project summary
        sim = compute_cosine_similarity(jd_vector, cand_emb)
        # GitScore combines SBERT semantic similarity with AST structural analysis when available
        ast_raw = cand.get("ast_structural_score") if cand.get("ast_structural_score") is not None else cand.get("ast_integrity_score")
        semantic_percentage = sim * 100.0
        if ast_raw is not None:
            ast_score = float(ast_raw)
            git_score = round((semantic_percentage * 0.90) + (ast_score * 0.10), 2)
        else:
            ast_score = None
            git_score = round(semantic_percentage, 2)
        git_score = min(100.0, max(0.0, git_score))

        # 3. Assessment test score (0 - 100)
        test_score = float(cand.get("test_score") or 0.0)

        # 4. Academic CGPA normalized (CGPA on 10.0 scale -> 0 to 100)
        cgpa = float(cand.get("cgpa") or 0.0)
        cgpa_normalized = round(min(100.0, max(0.0, cgpa * 10.0)), 2)

        # 5. Dynamic composite final score
        final_score = round(
            (test_score * norm_w_test) +
            (git_score * norm_w_git) +
            (cgpa_normalized * norm_w_acad),
            2
        )

        ranked_results.append({
            "candidate_id": cand.get("candidate_id") or cand.get("id"),
            "name": cand.get("name"),
            "college_id": cand.get("college_id"),
            "github_handle": cand.get("github_handle"),
            "cgpa": cgpa,
            "cgpa_normalized": cgpa_normalized,
            "test_score": test_score,
            "skill": cand.get("skill", "Fullstack / AI"),
            "git_score": git_score,
            "semantic_similarity": round(sim, 4),
            "similarity_percentage": round(sim * 100.0, 1),
            "ast_structural_score": ast_score,
            "ast_integrity_score": ast_score,
            "commit_count": cand.get("commit_count", 12),
            "project_title": cand.get("title", "Project"),
            "code_summary": cand.get("code_summary", ""),
            "final_score": final_score,
            "breakdown": {
                "test_contribution": round(test_score * norm_w_test, 2),
                "git_contribution": round(git_score * norm_w_git, 2),
                "acad_contribution": round(cgpa_normalized * norm_w_acad, 2),
                "weights_applied": {
                    "w_test": round(norm_w_test, 2),
                    "w_git": round(norm_w_git, 2),
                    "w_acad": round(norm_w_acad, 2),
                }
            }
        })

    # Sort descending by final composite score
    ranked_results.sort(key=lambda x: x["final_score"], reverse=True)

    # Assign 1-indexed ranks
    for rank_idx, cand_info in enumerate(ranked_results, start=1):
        cand_info["rank"] = rank_idx

    return ranked_results
