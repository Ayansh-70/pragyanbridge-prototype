"""
PragyanBridge Dynamic 70/20/10 Formula Calculator & Python AST Structural Analysis
SIH 2026 PS 26044 • Team Echelon
"""

import ast
from typing import Dict, Any, Tuple

def calculate_composite_score(
    test_score: float,
    git_score: float,
    cgpa: float,
    w_test: float = 0.70,
    w_git: float = 0.20,
    w_acad: float = 0.10
) -> Tuple[float, Dict[str, float]]:
    """
    Computes dynamic composite ranking score using the formula:
    Composite = (TestScore * w_test) + (GitScore * w_git) + (CGPA_Normalized * w_acad)
    """
    # Normalize weights so they sum to 1.0
    total_w = w_test + w_git + w_acad
    if total_w > 0:
        nw_test = w_test / total_w
        nw_git = w_git / total_w
        nw_acad = w_acad / total_w
    else:
        nw_test, nw_git, nw_acad = 0.70, 0.20, 0.10

    # Normalize CGPA (0-10 scale -> 0-100 scale)
    cgpa_normalized = min(100.0, max(0.0, cgpa * 10.0))

    # Calculate weighted contributions
    test_contrib = round(test_score * nw_test, 2)
    git_contrib = round(git_score * nw_git, 2)
    acad_contrib = round(cgpa_normalized * nw_acad, 2)

    final_score = round(test_contrib + git_contrib + acad_contrib, 2)

    breakdown = {
        "test_contribution": test_contrib,
        "git_contribution": git_contrib,
        "acad_contribution": acad_contrib,
        "w_test_applied": round(nw_test, 2),
        "w_git_applied": round(nw_git, 2),
        "w_acad_applied": round(nw_acad, 2)
    }

    return final_score, breakdown

def verify_ast_integrity(source_code: str) -> Dict[str, Any]:
    """
    Parses Python source code into an Abstract Syntax Tree (AST) and measures
    deterministic structural characteristics (modularity, node volume, and control flow).
    Note: AST analysis evaluates submitted code structure and syntax; it does not independently prove authorship.
    """
    if not source_code or not source_code.strip():
        return {
            "ast_valid": False,
            "ast_structural_score": None,
            "integrity_score": None,
            "error": "Actual source code was not provided for AST structural analysis.",
            "analysis_status": "VERIFICATION_UNAVAILABLE",
            "anti_cheat_status": "VERIFICATION_UNAVAILABLE",
            "authorship_verified": False,
            "note": "AST analysis evaluates submitted code structure and syntax; it does not independently prove authorship."
        }

    try:
        tree = ast.parse(source_code)
        nodes = list(ast.walk(tree))
        num_nodes = len(nodes)
        num_functions = len([n for n in nodes if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))])
        num_classes = len([n for n in nodes if isinstance(n, ast.ClassDef)])
        num_control = len([n for n in nodes if isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.With))])

        # Dynamic AST structural complexity calculation:
        # Trivial scripts without functions or classes have minimal structural completeness
        if num_functions == 0 and num_classes == 0:
            structural_score = round(min(45.0, max(15.0, num_nodes * 6.0)), 1)
            status = "STRUCTURAL_COMPLEXITY_MINIMAL"
        else:
            # Multi-component source: score scales proportionally from node volume, modularity, and control flow
            base_score = 60.0
            node_factor = min(15.0, num_nodes * 0.15)
            func_factor = min(12.0, num_functions * 2.0)
            class_factor = min(8.0, num_classes * 3.0)
            control_factor = min(5.0, num_control * 1.0)
            raw_score = base_score + node_factor + func_factor + class_factor + control_factor
            structural_score = round(min(99.5, max(50.0, raw_score)), 1)
            status = "STRUCTURAL_ANALYSIS_COMPLETE" if structural_score >= 85.0 else "STRUCTURAL_COMPLEXITY_MODERATE"

        return {
            "ast_valid": True,
            "ast_structural_score": structural_score,
            "integrity_score": structural_score,
            "ast_nodes_count": num_nodes,
            "functions_count": num_functions,
            "classes_count": num_classes,
            "control_structures_count": num_control,
            "analysis_status": status,
            "anti_cheat_status": status,
            "authorship_verified": False,
            "note": "AST analysis evaluates submitted code structure and syntax; it does not independently prove authorship."
        }
    except SyntaxError as e:
        return {
            "ast_valid": False,
            "ast_structural_score": None,
            "integrity_score": None,
            "error": f"SyntaxError at line {e.lineno}: {e.msg}",
            "analysis_status": "SYNTAX_ANOMALY_FLAGGED",
            "anti_cheat_status": "SYNTAX_ANOMALY_FLAGGED",
            "authorship_verified": False,
            "note": "AST analysis evaluates submitted code structure and syntax; it does not independently prove authorship."
        }

def get_candidate_source_representation(skill: str = "", title: str = "") -> str:
    """
    Reference / test-fixture utility returning sample Python source snippets
    corresponding to technical domains. NOT used in active candidate verification
    flows to prevent synthetic score fabrication.
    """
    skill_lower = (skill or "").lower()
    title_lower = (title or "").lower()

    if "fastapi" in skill_lower or "microservice" in skill_lower or "api" in title_lower:
        return '''"""FastAPI Asynchronous Pipeline Controller"""
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

class TaskPayload(BaseModel):
    task_id: str
    priority: int = Field(default=1, ge=1, le=5)
    payload_data: Dict[str, Any] = Field(default_factory=dict)

class AsynchronousWorkerPool:
    def __init__(self, pool_size: int = 8):
        self.pool_size = pool_size
        self.active_jobs = []

    async def dispatch_job(self, task: TaskPayload) -> Dict[str, Any]:
        self.active_jobs.append(task.task_id)
        return {"status": "dispatched", "worker_id": len(self.active_jobs) % self.pool_size}

    def get_pool_health(self) -> Dict[str, Any]:
        return {"active_count": len(self.active_jobs), "healthy": True}

app = FastAPI(title="DistributedTaskEngine")
pool = AsynchronousWorkerPool()

@app.post("/tasks/execute")
async def execute_task(task: TaskPayload):
    if not task.task_id:
        raise HTTPException(status_code=400, detail="Invalid task_id")
    return await pool.dispatch_job(task)

@app.get("/tasks/health")
async def pool_health():
    return pool.get_pool_health()
'''
    elif "pytorch" in skill_lower or "sbert" in skill_lower or "nlp" in skill_lower or "vision" in skill_lower:
        return '''"""PyTorch / SBERT Neural Embedding Pipeline"""
import torch
import torch.nn as nn
from typing import List, Optional

class DenseIntentEncoder(nn.Module):
    def __init__(self, embedding_dim: int = 384, hidden_dim: int = 512):
        super().__init__()
        self.linear1 = nn.Linear(embedding_dim, hidden_dim)
        self.activation = nn.ReLU()
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(hidden_dim, 64)

    def forward(self, input_vectors: torch.Tensor) -> torch.Tensor:
        h = self.dropout(self.activation(self.linear1(input_vectors)))
        return self.classifier(h)

class SemanticSimilarityIndex:
    def __init__(self, model: DenseIntentEncoder):
        self.model = model

    def score_similarity(self, vec_a: torch.Tensor, vec_b: torch.Tensor) -> float:
        cos = nn.CosineSimilarity(dim=0)
        return float(cos(vec_a, vec_b).item())
'''
    elif "crypto" in skill_lower or "security" in skill_lower:
        return '''"""Cryptographic SHA-256 Audit Signature Service"""
import hashlib
from typing import Dict, Any

class CredentialHasher:
    def __init__(self, salt: str = "PRAGYAN"):
        self.salt = salt

    def compute_audit_digest(self, candidate_id: str, score: float) -> str:
        payload = f"{self.salt}:{candidate_id}:{score:.2f}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def verify_audit_digest(self, candidate_id: str, score: float, digest: str) -> bool:
        expected = self.compute_audit_digest(candidate_id, score)
        return expected.lower() == digest.lower()
'''
    else:
        return '''"""Service Controller & Model Definition"""
from typing import Dict, Any, List

class CandidateProjectManager:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.modules = []

    def register_module(self, module_name: str) -> bool:
        if module_name not in self.modules:
            self.modules.append(module_name)
            return True
        return False

    def get_summary(self) -> Dict[str, Any]:
        return {"project": self.project_name, "modules_count": len(self.modules)}

def build_service(name: str) -> CandidateProjectManager:
    manager = CandidateProjectManager(name)
    manager.register_module("core")
    manager.register_module("api")
    return manager
'''
