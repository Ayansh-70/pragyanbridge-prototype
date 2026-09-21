"""
PragyanBridge Lightweight Extensible Skill Taxonomy & Extraction Engine
SIH 2026 PS 26044 • Team Echelon

Provides deterministic skill extraction from Job Descriptions (JDs) and
candidate profile/project records, along with factual skill-gap analysis.
"""

import re
from typing import Dict, List, Set, Any, Optional, Tuple

# ---------------------------------------------------------
# 1. Canonical Skill Taxonomy & Aliases
# ---------------------------------------------------------

# Canonical skill -> Category
SKILL_TAXONOMY: Dict[str, str] = {
    # Backend & Systems
    "Python": "Backend",
    "FastAPI": "Backend",
    "Node.js": "Backend",
    "Express": "Backend",
    "Go": "Backend",
    "Java": "Backend",
    "REST APIs": "Backend",
    "gRPC": "Backend",
    "GraphQL": "Backend",
    "WebSockets": "Backend",
    "Microservices": "Backend",

    # Frontend
    "React": "Frontend",
    "Next.js": "Frontend",
    "JavaScript": "Frontend",
    "TypeScript": "Frontend",
    "Tailwind CSS": "Frontend",

    # Databases & Caching
    "PostgreSQL": "Databases",
    "MongoDB": "Databases",
    "SQLite": "Databases",
    "Redis": "Databases",
    "SQL": "Databases",

    # Cloud, DevOps & Containers
    "Docker": "DevOps & Cloud",
    "Kubernetes": "DevOps & Cloud",
    "CI/CD": "DevOps & Cloud",
    "Git": "DevOps & Cloud",
    "Helm": "DevOps & Cloud",
    "Prometheus": "DevOps & Cloud",
    "Cloud Platforms": "DevOps & Cloud",

    # AI, ML & Data Engineering
    "PyTorch": "Data & AI",
    "TensorFlow": "Data & AI",
    "Scikit-Learn": "Data & AI",
    "Machine Learning": "Data & AI",
    "Natural Language Processing": "Data & AI",
    "SBERT / NLP": "Data & AI",
    "Apache Spark": "Data & AI",

    # Conceptual & Engineering Fundamentals
    "Data Structures & Algorithms": "Concepts",
    "System Design": "Concepts",
    "OOP": "Concepts",
    "Software Testing": "Concepts",
    "Asynchronous Programming": "Concepts",
}

CANONICAL_SKILLS: Set[str] = set(SKILL_TAXONOMY.keys())

# Aliases mapping (case-insensitive) -> Canonical skill
SKILL_ALIASES: Dict[str, str] = {
    # Python & Frameworks
    "python": "Python",
    "fastapi": "FastAPI",
    "fast api": "FastAPI",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "express": "Express",
    "express.js": "Express",
    "expressjs": "Express",
    "go": "Go",
    "golang": "Go",
    "java": "Java",
    "rest": "REST APIs",
    "restful": "REST APIs",
    "rest api": "REST APIs",
    "rest apis": "REST APIs",
    "restful api": "REST APIs",
    "restful apis": "REST APIs",
    "grpc": "gRPC",
    "graphql": "GraphQL",
    "websocket": "WebSockets",
    "websockets": "WebSockets",
    "microservice": "Microservices",
    "microservices": "Microservices",

    # Frontend
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    "next": "Next.js",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "tailwind css": "Tailwind CSS",

    # Databases
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "sqlite": "SQLite",
    "redis": "Redis",
    "sql": "SQL",

    # DevOps & Cloud
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "github actions": "CI/CD",
    "git": "Git",
    "helm": "Helm",
    "prometheus": "Prometheus",
    "cloud": "Cloud Platforms",
    "aws": "Cloud Platforms",
    "gcp": "Cloud Platforms",
    "azure": "Cloud Platforms",

    # AI & ML
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "tf": "TensorFlow",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "natural language processing": "Natural Language Processing",
    "nlp": "Natural Language Processing",
    "sbert": "SBERT / NLP",
    "sentence transformers": "SBERT / NLP",
    "sentence-transformers": "SBERT / NLP",
    "spark": "Apache Spark",
    "pyspark": "Apache Spark",
    "apache spark": "Apache Spark",

    # Concepts
    "dsa": "Data Structures & Algorithms",
    "data structures": "Data Structures & Algorithms",
    "algorithms": "Data Structures & Algorithms",
    "system design": "System Design",
    "oop": "OOP",
    "object oriented": "OOP",
    "testing": "Software Testing",
    "unit testing": "Software Testing",
    "software testing": "Software Testing",
    "async": "Asynchronous Programming",
    "asynchronous": "Asynchronous Programming",
    "asyncio": "Asynchronous Programming",
}

# Related skill groupings for partial match reasoning
RELATED_SKILLS: Dict[str, List[str]] = {
    "PostgreSQL": ["SQLite", "MongoDB", "SQL"],
    "MongoDB": ["PostgreSQL", "SQLite", "SQL"],
    "SQLite": ["PostgreSQL", "MongoDB", "SQL"],
    "FastAPI": ["Express", "Node.js", "REST APIs"],
    "Express": ["FastAPI", "Node.js", "REST APIs"],
    "React": ["Next.js", "TypeScript", "JavaScript"],
    "Next.js": ["React", "TypeScript", "JavaScript"],
    "Docker": ["Kubernetes", "CI/CD"],
    "Kubernetes": ["Docker", "CI/CD", "Helm"],
    "PyTorch": ["TensorFlow", "Scikit-Learn", "Machine Learning"],
    "TensorFlow": ["PyTorch", "Scikit-Learn", "Machine Learning"],
    "Apache Spark": ["Python", "Machine Learning"],
}

# ---------------------------------------------------------
# 2. Text Normalization & Matching Helpers
# ---------------------------------------------------------

def normalize_skill_name(raw_name: str) -> Optional[str]:
    """Resolves raw skill phrase to canonical name via taxonomy and aliases."""
    clean = raw_name.strip().lower()
    if clean in SKILL_ALIASES:
        return SKILL_ALIASES[clean]
    # Direct case-insensitive match against canonical taxonomy keys
    for canonical in SKILL_TAXONOMY:
        if canonical.lower() == clean:
            return canonical
    return None

resolve_skill_alias = normalize_skill_name

def get_related_skills(skill: str) -> List[str]:
    """Returns list of related skills for partial match analysis."""
    return RELATED_SKILLS.get(skill, [])

def extract_tokens_and_phrases(text: str) -> Set[str]:
    """Generates set of unigrams, bigrams, and trigrams from normalized text."""
    # Retain characters like '.', '/', '-', '+'
    cleaned = re.sub(r"[^\w\s\.\/\-\+]", " ", text.lower())
    words = cleaned.split()
    phrases = set(words)

    # Bigrams
    for i in range(len(words) - 1):
        phrases.add(f"{words[i]} {words[i+1]}")
    # Trigrams
    for i in range(len(words) - 2):
        phrases.add(f"{words[i]} {words[i+1]} {words[i+2]}")

    return phrases

# ---------------------------------------------------------
# 3. Job Description Skill Extraction
# ---------------------------------------------------------

def extract_jd_skills(jd_text: str) -> Dict[str, Any]:
    """
    Deterministically parses role, required skills, preferred skills,
    and responsibilities from recruiter Job Description text.
    """
    if not jd_text or not jd_text.strip():
        return {
            "role": "Software Engineer",
            "required_skills": [],
            "preferred_skills": [],
            "responsibilities": ["General software development and delivery"],
            "experience_level": "Entry / Early Career"
        }

    phrases = extract_tokens_and_phrases(jd_text)
    extracted_required: Set[str] = set()

    # Search for canonical skills and aliases in the JD text
    for phrase in phrases:
        norm = normalize_skill_name(phrase)
        if norm:
            extracted_required.add(norm)

    # Direct regex check for short/distinct symbols that might miss phrase splitting
    for alias, canonical in SKILL_ALIASES.items():
        pattern = r"\b" + re.escape(alias) + r"\b"
        if re.search(pattern, jd_text, re.IGNORECASE):
            extracted_required.add(canonical)

    # Sort deterministically
    required_skills = sorted(list(extracted_required))

    # Detect role from text
    role = "Software Engineer"
    text_lower = jd_text.lower()
    if "backend" in text_lower or "api" in text_lower:
        role = "Backend Developer"
    elif "fullstack" in text_lower or "full stack" in text_lower or "full-stack" in text_lower:
        role = "Full Stack Developer"
    elif "frontend" in text_lower or "react" in text_lower:
        role = "Frontend Developer"
    elif "machine learning" in text_lower or "nlp" in text_lower or "ai" in text_lower or "data science" in text_lower:
        role = "Machine Learning Engineer"
    elif "devops" in text_lower or "cloud" in text_lower or "kubernetes" in text_lower:
        role = "DevOps & Cloud Engineer"
    elif "data" in text_lower or "spark" in text_lower:
        role = "Data Engineer"

    # Responsibilities derived from text segments
    responsibilities = []
    sentences = [s.strip() for s in re.split(r"[\.\n\r;]", jd_text) if len(s.strip()) > 15]
    for s in sentences[:3]:
        # Filter sentences that look like tasks
        if any(w in s.lower() for w in ["build", "develop", "maintain", "deploy", "design", "implement", "experience", "work"]):
            responsibilities.append(s[:100].strip())
    if not responsibilities:
        responsibilities = [f"Design and deploy {role.lower()} components using {', '.join(required_skills[:3]) if required_skills else 'modern frameworks'}"]

    return {
        "role": role,
        "required_skills": required_skills,
        "preferred_skills": [],
        "responsibilities": responsibilities,
        "experience_level": "Entry / Early Career (B.Tech 2026)"
    }

# ---------------------------------------------------------
# 4. Candidate Skill Extraction (with Provenance)
# ---------------------------------------------------------

def extract_candidate_skills(candidate_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extracts verified candidate skills from existing database records:
    - scores.skill (assessment tested skill)
    - projects.title
    - projects.description
    - projects.code_summary
    Preserves exact provenance without fabricating unsupported skills.
    """
    candidate_skills_map: Dict[str, Dict[str, Any]] = {}

    def add_skill(canonical: str, source: str, snippet: str = ""):
        if canonical not in candidate_skills_map:
            candidate_skills_map[canonical] = {
                "skill": canonical,
                "category": SKILL_TAXONOMY.get(canonical, "General"),
                "provenance": []
            }
        if source not in [p["source"] for p in candidate_skills_map[canonical]["provenance"]]:
            candidate_skills_map[canonical]["provenance"].append({
                "source": source,
                "evidence": snippet[:80].strip() if snippet else source
            })

    # 1. Assessment Skill (scores table)
    assessment_skill = candidate_dict.get("skill") or ""
    if assessment_skill:
        for phrase in extract_tokens_and_phrases(assessment_skill):
            norm = normalize_skill_name(phrase)
            if norm:
                add_skill(norm, "proctored_assessment", assessment_skill)
        for alias, canonical in SKILL_ALIASES.items():
            if re.search(r"\b" + re.escape(alias) + r"\b", assessment_skill, re.IGNORECASE):
                add_skill(canonical, "proctored_assessment", assessment_skill)

    # 2. Project Title
    proj_title = candidate_dict.get("project_title") or candidate_dict.get("title") or ""
    if proj_title:
        for alias, canonical in SKILL_ALIASES.items():
            if re.search(r"\b" + re.escape(alias) + r"\b", proj_title, re.IGNORECASE):
                add_skill(canonical, "project_title", proj_title)

    # 3. Project Description
    proj_desc = candidate_dict.get("project_description") or candidate_dict.get("description") or ""
    if proj_desc:
        for alias, canonical in SKILL_ALIASES.items():
            if re.search(r"\b" + re.escape(alias) + r"\b", proj_desc, re.IGNORECASE):
                add_skill(canonical, "project_description", proj_desc)

    # 4. Project Code Summary
    code_summary = candidate_dict.get("code_summary") or ""
    if code_summary:
        for alias, canonical in SKILL_ALIASES.items():
            if re.search(r"\b" + re.escape(alias) + r"\b", code_summary, re.IGNORECASE):
                add_skill(canonical, "project_code_summary", code_summary)

    # 5. Support nested 'projects' list if provided
    for proj in candidate_dict.get("projects", []):
        if isinstance(proj, dict):
            p_title = proj.get("title", "")
            p_desc = proj.get("description", "")
            p_code = proj.get("code_summary", "")
            for text_val, src in [(p_title, "project_title"), (p_desc, "project_description"), (p_code, "project_code_summary")]:
                if text_val:
                    for alias, canonical in SKILL_ALIASES.items():
                        if re.search(r"\b" + re.escape(alias) + r"\b", text_val, re.IGNORECASE):
                            add_skill(canonical, src, text_val)

    # 6. Support nested 'scores' list if provided
    for score_item in candidate_dict.get("scores", []):
        if isinstance(score_item, dict):
            s_skill = score_item.get("skill", "")
            if s_skill:
                for alias, canonical in SKILL_ALIASES.items():
                    if re.search(r"\b" + re.escape(alias) + r"\b", s_skill, re.IGNORECASE):
                        add_skill(canonical, "proctored_assessment", s_skill)

    return sorted(list(candidate_skills_map.values()), key=lambda x: x["skill"])

# ---------------------------------------------------------
# 5. Deterministic Skill Gap & Coverage Engine
# ---------------------------------------------------------

def compute_skill_gap(
    required_skills: List[str],
    candidate_skills_data: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes factual, deterministic skill matches, missing skills, partial matches,
    and coverage percentage with alias normalization and deduplication.
    """
    # 1. Normalize and deduplicate required skills
    normalized_req: List[str] = []
    for r in required_skills:
        canonical = normalize_skill_name(r) or str(r).strip()
        if canonical and canonical not in normalized_req:
            normalized_req.append(canonical)
    req_skill_set = set(normalized_req)

    # 2. Normalize candidate skills set
    cand_skill_names = set()
    for c in candidate_skills_data:
        raw = c["skill"] if isinstance(c, dict) else str(c)
        canonical = normalize_skill_name(raw) or str(raw).strip()
        if canonical:
            cand_skill_names.add(canonical)

    matched_skills = sorted(list(req_skill_set.intersection(cand_skill_names)))
    missing_skills = sorted(list(req_skill_set - cand_skill_names))

    # Identify partial / related technology matches
    partial_matches = []
    for missing in missing_skills:
        related_candidates = RELATED_SKILLS.get(missing, [])
        for related in related_candidates:
            if related in cand_skill_names:
                partial_matches.append({
                    "required_skill": missing,
                    "candidate_has": related,
                    "category": SKILL_TAXONOMY.get(missing, "General"),
                    "relationship": f"Experience in {related} provides conceptual foundation for {missing}"
                })
                break

    # Deterministic Skill Coverage %
    if normalized_req:
        coverage = round((len(matched_skills) / len(normalized_req)) * 100.0, 1)
    else:
        coverage = 100.0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "partial_matches": partial_matches,
        "matched_count": len(matched_skills),
        "missing_count": len(missing_skills),
        "total_required_count": len(normalized_req),
        "skill_coverage": coverage
    }


def compute_institutional_skill_gap(
    candidates_list: List[Dict[str, Any]],
    required_skills: List[str]
) -> Dict[str, Any]:
    """
    Computes institutional skill coverage across a student cohort against required skills.
    Disambiguates:
    - per_skill_coverage: (candidates with skill / total candidates) * 100
    - overall_institutional_coverage: (sum of candidate-skill matches) / (unique required skills * total candidates) * 100
    Handles edge cases:
    - 0 candidates -> 0.0%
    - 0 required skills -> 0.0%
    - Duplicate skills & aliases -> normalized to unique canonical taxonomy skills
    """
    total_candidates = len(candidates_list)

    # 1. Normalize and deduplicate required skills using taxonomy & aliases
    normalized_required: List[str] = []
    for r in required_skills:
        canonical = normalize_skill_name(r) or str(r).strip()
        if canonical and canonical not in normalized_required:
            normalized_required.append(canonical)
    normalized_required.sort()

    if total_candidates == 0 or len(normalized_required) == 0:
        return {
            "required_skills": normalized_required,
            "total_candidates": total_candidates,
            "overall_institutional_coverage": 0.0,
            "institutional_coverage": 0.0,
            "total_skill_matches": 0,
            "total_possible_matches": 0,
            "skill_breakdown": [],
            "highest_coverage_skills": [],
            "largest_gap_skills": [],
            "coverage_metric_explanation": "Overall coverage = total skill matches / (unique required skills * total candidates). Per-skill coverage = candidates with skill / total candidates."
        }

    skill_breakdown = []
    total_skill_matches = 0

    for req_sk in normalized_required:
        covered_cands = []
        missing_cands = []
        for cand in candidates_list:
            # Extract skills if not already attached
            if "extracted_skills" in cand and isinstance(cand["extracted_skills"], list):
                cand_skills = [s["skill"] if isinstance(s, dict) else str(s) for s in cand["extracted_skills"]]
            else:
                cand_extracted = extract_candidate_skills(cand)
                cand_skills = [s["skill"] for s in cand_extracted]

            # Normalize candidate skills to canonical names
            cand_canonicals = set()
            for cs in cand_skills:
                norm_cs = normalize_skill_name(cs) or cs
                cand_canonicals.add(norm_cs)

            if req_sk in cand_canonicals:
                covered_cands.append({
                    "id": cand.get("id"),
                    "name": cand.get("name"),
                    "college_id": cand.get("college_id")
                })
            else:
                missing_cands.append({
                    "id": cand.get("id"),
                    "name": cand.get("name"),
                    "college_id": cand.get("college_id")
                })

        cov_count = len(covered_cands)
        missing_count = len(missing_cands)
        cov_pct = round((cov_count / total_candidates) * 100, 1)
        total_skill_matches += cov_count

        skill_breakdown.append({
            "skill": req_sk,
            "category": SKILL_TAXONOMY.get(req_sk, "General"),
            "covered_count": cov_count,
            "missing_count": missing_count,
            "coverage_percentage": cov_pct,
            "covered_candidates": covered_cands,
            "missing_candidates": missing_cands
        })

    total_possible = total_candidates * len(normalized_required)
    overall_coverage = round((total_skill_matches / total_possible) * 100, 1) if total_possible > 0 else 0.0

    highest_coverage = sorted(skill_breakdown, key=lambda x: x["coverage_percentage"], reverse=True)[:3]
    largest_gaps = sorted(skill_breakdown, key=lambda x: x["coverage_percentage"])[:3]

    return {
        "required_skills": normalized_required,
        "total_candidates": total_candidates,
        "overall_institutional_coverage": overall_coverage,
        "institutional_coverage": overall_coverage,
        "total_skill_matches": total_skill_matches,
        "total_possible_matches": total_possible,
        "skill_breakdown": skill_breakdown,
        "highest_coverage_skills": highest_coverage,
        "largest_gap_skills": largest_gaps,
        "coverage_metric_explanation": "Overall coverage = total skill matches / (unique required skills * total candidates). Per-skill coverage = candidates with skill / total candidates."
    }

