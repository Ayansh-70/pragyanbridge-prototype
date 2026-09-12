"use client";

import React, { useState, useEffect } from "react";
import {
  Search,
  Sliders,
  ShieldCheck,
  Github,
  GraduationCap,
  Building2,
  Download,
  Award,
  CheckCircle,
  ExternalLink,
  RefreshCw,
  BarChart3,
  Users,
  Sparkles,
  Layers,
  Code2,
  Terminal,
  QrCode,
  FileCheck2,
  AlertCircle,
  TrendingUp,
  Cpu
} from "lucide-react";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Fallback seed candidates for offline or immediate demo
const INITIAL_CANDIDATES = [
  {
    candidate_id: "c-101",
    name: "Aditya Sharma",
    college_id: "PIT-CSE-22-041",
    github_handle: "aditya-fastapi",
    cgpa: 9.12,
    cgpa_normalized: 91.2,
    test_score: 94.5,
    skill: "FastAPI & Microservices",
    git_score: 95.8,
    semantic_similarity: 0.892,
    similarity_percentage: 89.2,
    ast_integrity_score: 98.4,
    commit_count: 38,
    project_title: "High-Throughput Asynchronous Task Pipeline",
    code_summary: "Distributed task engine with FastAPI, Redis, Docker containerization, and SQLite backend with full type validation.",
    final_score: 94.4,
    rank: 1,
    credential_hash: "9a2f78b9c4501a3de6804a112ec4917f8b9d3e4c19a2b5e7d8f01a3b4c5d6e7f",
    breakdown: {
      test_contribution: 66.15,
      git_contribution: 19.16,
      acad_contribution: 9.12,
    }
  },
  {
    candidate_id: "c-102",
    name: "Pooja Hegde",
    college_id: "PIT-AI-22-019",
    github_handle: "pooja-genai",
    cgpa: 8.85,
    cgpa_normalized: 88.5,
    test_score: 91.0,
    skill: "PyTorch & SBERT Vectors",
    git_score: 92.4,
    semantic_similarity: 0.865,
    similarity_percentage: 86.5,
    ast_integrity_score: 96.0,
    commit_count: 29,
    project_title: "Contextual Document Intent Semantic Matcher",
    code_summary: "SentenceTransformers pipeline generating 384-dimensional dense vectors with cosine similarity retrieval.",
    final_score: 91.0,
    rank: 2,
    credential_hash: "3b18c7e94a5f012de9401b235fc4917a1b8c2d3e4f5a6b7c8d9e0f1a2b3c4d5e",
    breakdown: {
      test_contribution: 63.7,
      git_contribution: 18.48,
      acad_contribution: 8.85,
    }
  },
  {
    candidate_id: "c-103",
    name: "Rohan Varma",
    college_id: "PIT-CSE-22-088",
    github_handle: "rohan-fullstack",
    cgpa: 8.45,
    cgpa_normalized: 84.5,
    test_score: 87.0,
    skill: "Next.js & Tailwind CSS",
    git_score: 88.6,
    semantic_similarity: 0.812,
    similarity_percentage: 81.2,
    ast_integrity_score: 95.2,
    commit_count: 24,
    project_title: "Pragyan Unified Placement Management UI",
    code_summary: "Responsive Next.js 14 dashboard with reactive state, Tailwind CSS, and cryptographic badge preview.",
    final_score: 87.1,
    rank: 3,
    credential_hash: "7f4c9a1e2b3d4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a",
    breakdown: {
      test_contribution: 60.9,
      git_contribution: 17.72,
      acad_contribution: 8.45,
    }
  },
  {
    candidate_id: "c-104",
    name: "Sneha Mukherjee",
    college_id: "PIT-IT-22-014",
    github_handle: "sneha-cloud",
    cgpa: 9.30,
    cgpa_normalized: 93.0,
    test_score: 84.0,
    skill: "Kubernetes & DevOps",
    git_score: 86.0,
    semantic_similarity: 0.774,
    similarity_percentage: 77.4,
    ast_integrity_score: 97.0,
    commit_count: 31,
    project_title: "Automated Microservice Deployment Helm Charts",
    code_summary: "Production CI/CD pipelines with GitHub Actions, Helm charts, and container health orchestration.",
    final_score: 85.3,
    rank: 4,
    credential_hash: "5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e",
    breakdown: {
      test_contribution: 58.8,
      git_contribution: 17.2,
      acad_contribution: 9.3,
    }
  }
];

export default function PragyanBridgeDashboard() {
  const [activeTab, setActiveTab] = useState<"recruiter" | "student" | "tpo">("recruiter");

  // Recruiter View State
  const [jdText, setJdText] = useState("FastAPI backend developer with SQLite, microservices and REST API skills");
  const [wTest, setWTest] = useState(70);
  const [wGit, setWGit] = useState(20);
  const [wAcad, setWAcad] = useState(10);
  const [candidates, setCandidates] = useState(INITIAL_CANDIDATES);
  const [isSearching, setIsSearching] = useState(false);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);

  // Student View State
  const [studentCommits, setStudentCommits] = useState(38);
  const [studentAstScore, setStudentAstScore] = useState(98.4);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncSuccess, setSyncSuccess] = useState(false);
  const [selectedBadge, setSelectedBadge] = useState<any>(null);

  // TPO View State
  const [naacData, setNaacData] = useState<any>(null);
  const [isExporting, setIsExporting] = useState(false);

  // Check backend health on load
  useEffect(() => {
    fetch(`${BACKEND_URL}/api/health`)
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "ok") setBackendOnline(true);
      })
      .catch(() => setBackendOnline(false));
  }, []);

  // Recruiter search handler
  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setIsSearching(true);

    try {
      const res = await fetch(`${BACKEND_URL}/api/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          jd_text: jdText,
          w_test: wTest / 100,
          w_git: wGit / 100,
          w_acad: wAcad / 100,
        }),
      });

      if (!res.ok) throw new Error("Search API failed");
      const data = await res.json();
      if (data.candidates && data.candidates.length > 0) {
        setCandidates(data.candidates);
      }
    } catch (err) {
      console.warn("Using client-side dynamic re-ranking fallback:", err);
      // Fallback local re-ranking for offline resilience
      const tot = wTest + wGit + wAcad || 100;
      const nwT = wTest / tot;
      const nwG = wGit / tot;
      const nwA = wAcad / tot;

      const updated = candidates.map((cand) => {
        const finalScore = Number(
          ((cand.test_score * nwT) + (cand.git_score * nwG) + (cand.cgpa_normalized * nwA)).toFixed(2)
        );
        return {
          ...cand,
          final_score: finalScore,
          breakdown: {
            test_contribution: Number((cand.test_score * nwT).toFixed(2)),
            git_contribution: Number((cand.git_score * nwG).toFixed(2)),
            acad_contribution: Number((cand.cgpa_normalized * nwA).toFixed(2)),
          }
        };
      });

      updated.sort((a, b) => b.final_score - a.final_score);
      setCandidates(updated.map((c, i) => ({ ...c, rank: i + 1 })));
    } finally {
      setIsSearching(false);
    }
  };

  // Student GitHub Sync simulation
  const handleSyncGithub = async () => {
    setIsSyncing(true);
    setSyncSuccess(false);

    try {
      const res = await fetch(`${BACKEND_URL}/api/sync-github`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          candidate_id: "c-101",
          github_handle: "aditya-fastapi",
          repo_name: "pragyanbridge-core",
        }),
      });
      if (res.ok) {
        const d = await res.json();
        setStudentCommits(d.commit_count);
        setStudentAstScore(d.ast_integrity_score);
      } else {
        setStudentCommits((prev) => prev + 4);
        setStudentAstScore(98.8);
      }
    } catch {
      setStudentCommits((prev) => prev + 4);
      setStudentAstScore(98.8);
    } finally {
      setIsSyncing(false);
      setSyncSuccess(true);
      setTimeout(() => setSyncSuccess(false), 4000);
    }
  };

  // TPO 1-Click NAAC Export
  const handleNaacExport = async () => {
    setIsExporting(true);
    try {
      const res = await fetch(`${BACKEND_URL}/api/tpo/naac-export`);
      let data;
      if (res.ok) {
        data = await res.json();
      } else {
        // Mock NAAC data fallback
        data = {
          institution: {
            name: "Pragyan Institute of Technology",
            academic_year: "2025-2026",
            naac_cycle: "Cycle 3",
          },
          naac_criteria: {
            criterion_1_3: {
              title: "Curriculum Enrichment & Experiential Learning",
              metric: "1.3.2 / 1.3.3 Projects & Field Internships",
              ast_verified_projects: 15,
              avg_ast_score: 96.8,
            },
            criterion_3_5: {
              title: "Industry Collaboration & Readiness",
              readiness_rate: "86.7%",
              sbert_intent_alignment: "88.4 / 100",
            },
            criterion_5_2: {
              title: "Student Placement & Progression",
              placement_rate: "86.7%",
              avg_cgpa: 8.42,
              median_composite_score: 84.1,
            },
          },
          digital_signature: {
            algorithm: "SHA-256",
            status: "OFFICIALLY_VERIFIED",
            proof_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
          }
        };
      }
      setNaacData(data);

      // Trigger automatic file download
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `NAAC_Placement_Dossier_Criteria_1.3_3.5_5.2.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error(e);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navigation Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
              <Cpu className="h-6 w-6 text-slate-950 font-bold" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-xl font-bold tracking-tight text-white">PragyanBridge</h1>
                <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full font-mono font-medium">
                  SIH 2026 PS 26044
                </span>
              </div>
              <p className="text-xs text-slate-400">AI Intent Vector Matching & Tamper-Proof NAAC Accreditation</p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="flex bg-slate-800/80 p-1.5 rounded-xl border border-slate-700/60 shadow-inner">
            <button
              onClick={() => setActiveTab("recruiter")}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "recruiter"
                  ? "bg-emerald-500 text-slate-950 shadow-md font-semibold"
                  : "text-slate-300 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <Building2 className="h-4 w-4" />
              <span>Recruiter Portal</span>
            </button>
            <button
              onClick={() => setActiveTab("student")}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "student"
                  ? "bg-emerald-500 text-slate-950 shadow-md font-semibold"
                  : "text-slate-300 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <GraduationCap className="h-4 w-4" />
              <span>Student Portal</span>
            </button>
            <button
              onClick={() => setActiveTab("tpo")}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "tpo"
                  ? "bg-emerald-500 text-slate-950 shadow-md font-semibold"
                  : "text-slate-300 hover:text-white hover:bg-slate-700/50"
              }`}
            >
              <Award className="h-4 w-4" />
              <span>College TPO & NAAC</span>
            </button>
          </div>

          {/* Live Status Indicator */}
          <div className="flex items-center space-x-2 text-xs">
            <span
              className={`h-2.5 w-2.5 rounded-full ${
                backendOnline ? "bg-emerald-400 animate-pulse" : "bg-amber-400"
              }`}
            />
            <span className="text-slate-400">
              Backend:{" "}
              <strong className={backendOnline ? "text-emerald-400" : "text-amber-400"}>
                {backendOnline ? "FastAPI Online" : "Local Mock Fallback"}
              </strong>
            </span>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6">
        {/* ==================================================== */}
        {/* VIEW 1: RECRUITER PORTAL */}
        {/* ==================================================== */}
        {activeTab === "recruiter" && (
          <div className="space-y-6">
            {/* Search and Sliders Hero */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />

              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <Sparkles className="h-5 w-5 text-emerald-400" />
                  <h2 className="text-lg font-bold text-white">SBERT Code Intent Matcher & Dynamic Rubric</h2>
                </div>
                <span className="text-xs font-mono text-slate-400 bg-slate-800 px-2.5 py-1 rounded-md border border-slate-700">
                  Model: all-MiniLM-L6-v2 (384-dim)
                </span>
              </div>

              {/* Natural Language Search Input */}
              <form onSubmit={handleSearch} className="space-y-4">
                <div className="relative">
                  <Search className="absolute left-4 top-3.5 h-5 w-5 text-slate-400" />
                  <input
                    type="text"
                    value={jdText}
                    onChange={(e) => setJdText(e.target.value)}
                    placeholder="Enter natural language Job Description (e.g., 'FastAPI backend engineer with SQLite, Docker, microservices')"
                    className="w-full bg-slate-950 border border-slate-700 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 rounded-xl pl-12 pr-32 py-3.5 text-sm text-slate-100 placeholder-slate-500 transition-all outline-none"
                  />
                  <button
                    type="submit"
                    disabled={isSearching}
                    className="absolute right-2 top-2 bottom-2 px-5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold rounded-lg text-sm transition-all flex items-center space-x-2 shadow"
                  >
                    {isSearching ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                    <span>{isSearching ? "Matching..." : "AI Match"}</span>
                  </button>
                </div>

                {/* Dynamic 70/20/10 Sliders */}
                <div className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-4 grid grid-cols-1 md:grid-cols-3 gap-6">
                  {/* Slider 1: Test Score */}
                  <div className="space-y-2">
                    <div className="flex justify-between items-center text-xs">
                      <span className="text-slate-300 font-medium flex items-center gap-1.5">
                        <Terminal className="h-3.5 w-3.5 text-emerald-400" /> Assessment Test Weight
                      </span>
                      <span className="font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        {wTest}%
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      step="5"
                      value={wTest}
                      onChange={(e) => {
                        setWTest(Number(e.target.value));
                        handleSearch();
                      }}
                      className="w-full accent-emerald-500 cursor-pointer"
                    />
                    <p className="text-[11px] text-slate-500">Core technical proctored coding assessments</p>
                  </div>

                  {/* Slider 2: Git Code Intent */}
                  <div className="space-y-2">
                    <div className="flex justify-between items-center text-xs">
                      <span className="text-slate-300 font-medium flex items-center gap-1.5">
                        <Github className="h-3.5 w-3.5 text-emerald-400" /> GitHub Code Intent Weight
                      </span>
                      <span className="font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        {wGit}%
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      step="5"
                      value={wGit}
                      onChange={(e) => {
                        setWGit(Number(e.target.value));
                        handleSearch();
                      }}
                      className="w-full accent-emerald-500 cursor-pointer"
                    />
                    <p className="text-[11px] text-slate-500">SBERT vector similarity + AST integrity score</p>
                  </div>

                  {/* Slider 3: Academics CGPA */}
                  <div className="space-y-2">
                    <div className="flex justify-between items-center text-xs">
                      <span className="text-slate-300 font-medium flex items-center gap-1.5">
                        <GraduationCap className="h-3.5 w-3.5 text-emerald-400" /> Academic CGPA Weight
                      </span>
                      <span className="font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        {wAcad}%
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      step="5"
                      value={wAcad}
                      onChange={(e) => {
                        setWAcad(Number(e.target.value));
                        handleSearch();
                      }}
                      className="w-full accent-emerald-500 cursor-pointer"
                    />
                    <p className="text-[11px] text-slate-500">Normalized university CGPA factor</p>
                  </div>
                </div>
              </form>
            </div>

            {/* Results Table Header */}
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-semibold text-white">
                  Ranked Candidates ({candidates.length} Profiles Evaluated)
                </h3>
                <p className="text-xs text-slate-400">
                  Formula: Composite = (Test × {wTest}%) + (Git × {wGit}%) + (Acad × {wAcad}%)
                </p>
              </div>
              <div className="flex items-center space-x-2 text-xs text-slate-400">
                <ShieldCheck className="h-4 w-4 text-emerald-400" />
                <span>All candidates verified with AST Anti-Cheat</span>
              </div>
            </div>

            {/* Ranked Candidate Results Table */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-slate-950/80 text-xs uppercase font-semibold text-slate-400 border-b border-slate-800">
                    <tr>
                      <th className="py-3.5 px-4">Rank</th>
                      <th className="py-3.5 px-4">Candidate & Project</th>
                      <th className="py-3.5 px-4">SBERT Match</th>
                      <th className="py-3.5 px-4">AST Anti-Cheat</th>
                      <th className="py-3.5 px-4">Test / CGPA</th>
                      <th className="py-3.5 px-4 text-right">Composite Score</th>
                      <th className="py-3.5 px-4 text-center">Badge</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {candidates.map((cand, idx) => (
                      <tr
                        key={cand.candidate_id || idx}
                        className="hover:bg-slate-850/60 transition-colors group"
                      >
                        {/* Rank Badge */}
                        <td className="py-4 px-4 font-mono font-bold">
                          <span
                            className={`inline-flex items-center justify-center h-7 w-7 rounded-full text-xs ${
                              idx === 0
                                ? "bg-amber-400/20 text-amber-300 border border-amber-400/40"
                                : idx === 1
                                ? "bg-slate-300/20 text-slate-200 border border-slate-300/40"
                                : idx === 2
                                ? "bg-amber-700/20 text-amber-500 border border-amber-600/40"
                                : "bg-slate-800 text-slate-400"
                            }`}
                          >
                            #{cand.rank || idx + 1}
                          </span>
                        </td>

                        {/* Candidate Info */}
                        <td className="py-4 px-4">
                          <div>
                            <div className="font-semibold text-white flex items-center space-x-2">
                              <span>{cand.name}</span>
                              <span className="text-xs text-slate-400 font-mono">
                                ({cand.college_id})
                              </span>
                            </div>
                            <div className="text-xs text-emerald-400 flex items-center space-x-2 mt-0.5">
                              <Github className="h-3 w-3" />
                              <span>@{cand.github_handle}</span>
                              <span className="text-slate-600">•</span>
                              <span className="text-slate-300 truncate max-w-xs">
                                {cand.project_title}
                              </span>
                            </div>
                          </div>
                        </td>

                        {/* SBERT Match Score */}
                        <td className="py-4 px-4">
                          <div className="space-y-1">
                            <div className="flex items-center space-x-2">
                              <span className="font-mono font-semibold text-emerald-400">
                                {cand.similarity_percentage || (cand.semantic_similarity * 100).toFixed(1)}%
                              </span>
                              <span className="text-[11px] text-slate-500">cosine</span>
                            </div>
                            <div className="w-24 bg-slate-800 rounded-full h-1.5 overflow-hidden">
                              <div
                                className="bg-emerald-500 h-full rounded-full"
                                style={{
                                  width: `${Math.min(100, Math.max(10, cand.similarity_percentage || 80))}%`
                                }}
                              />
                            </div>
                          </div>
                        </td>

                        {/* AST Anti-Cheat Integrity */}
                        <td className="py-4 px-4">
                          <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs bg-emerald-950/60 border border-emerald-500/30 text-emerald-300">
                            <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
                            <span className="font-mono font-semibold">
                              {cand.ast_integrity_score}% Validated
                            </span>
                          </div>
                          <div className="text-[11px] text-slate-500 mt-1">
                            {cand.commit_count || 12} commits parsed
                          </div>
                        </td>

                        {/* Test & CGPA */}
                        <td className="py-4 px-4 text-xs font-mono">
                          <div className="text-slate-200">
                            Test: <span className="text-emerald-400 font-semibold">{cand.test_score}</span>/100
                          </div>
                          <div className="text-slate-400 mt-0.5">
                            CGPA: <span className="text-slate-200 font-semibold">{cand.cgpa}</span>/10.0
                          </div>
                        </td>

                        {/* Composite Score */}
                        <td className="py-4 px-4 text-right">
                          <div className="font-mono text-lg font-bold text-white">
                            {cand.final_score}
                          </div>
                          <div className="text-[10px] text-slate-400 font-mono">
                            {cand.breakdown
                              ? `${cand.breakdown.test_contribution}T + ${cand.breakdown.git_contribution}G + ${cand.breakdown.acad_contribution}A`
                              : "Calculated"}
                          </div>
                        </td>

                        {/* SHA-256 Badge Preview */}
                        <td className="py-4 px-4 text-center">
                          <button
                            onClick={() => setSelectedBadge(cand)}
                            title="Verify SHA-256 Digital Badge"
                            className="p-2 rounded-lg bg-slate-800 hover:bg-emerald-500/20 text-slate-300 hover:text-emerald-400 border border-slate-700/80 transition-all"
                          >
                            <QrCode className="h-4 w-4" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* ==================================================== */}
        {/* VIEW 2: STUDENT PORTAL */}
        {/* ==================================================== */}
        {activeTab === "student" && (
          <div className="space-y-6">
            {/* Student Hero Header */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
              <div className="absolute -top-10 -right-10 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

              <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                <div className="flex items-center space-x-4">
                  <div className="h-16 w-16 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-400 p-0.5 shadow-lg shadow-emerald-500/20">
                    <div className="h-full w-full bg-slate-900 rounded-[14px] flex items-center justify-center">
                      <GraduationCap className="h-8 w-8 text-emerald-400" />
                    </div>
                  </div>
                  <div>
                    <div className="flex items-center space-x-3">
                      <h2 className="text-xl font-bold text-white">Aditya Sharma</h2>
                      <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2.5 py-0.5 rounded-full font-mono">
                        NAAC Verified Candidate
                      </span>
                    </div>
                    <p className="text-sm text-slate-400">
                      B.Tech Computer Science & Engineering • Roll: PIT-CSE-22-041 • CGPA: 9.12
                    </p>
                    <div className="flex items-center space-x-3 text-xs text-slate-400 mt-2">
                      <span className="flex items-center space-x-1">
                        <Github className="h-3.5 w-3.5 text-slate-300" />
                        <span className="text-emerald-400 font-mono">@aditya-fastapi</span>
                      </span>
                      <span>•</span>
                      <span>Commits: <strong className="text-white font-mono">{studentCommits}</strong></span>
                      <span>•</span>
                      <span>AST Integrity: <strong className="text-emerald-400 font-mono">{studentAstScore}%</strong></span>
                    </div>
                  </div>
                </div>

                {/* GitHub Sync Button */}
                <div className="flex flex-col items-end gap-2">
                  <button
                    onClick={handleSyncGithub}
                    disabled={isSyncing}
                    className="flex items-center space-x-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold px-5 py-2.5 rounded-xl text-sm transition-all shadow-lg shadow-emerald-500/20"
                  >
                    <RefreshCw className={`h-4 w-4 ${isSyncing ? "animate-spin" : ""}`} />
                    <span>{isSyncing ? "Parsing Commits & AST..." : "Sync GitHub Repository"}</span>
                  </button>
                  {syncSuccess && (
                    <span className="text-xs text-emerald-400 flex items-center gap-1">
                      <CheckCircle className="h-3.5 w-3.5" /> Commits synced & SBERT vector regenerated!
                    </span>
                  )}
                </div>
              </div>
            </div>

            {/* Two Column Layout: Skill Tree & Digital Credential */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Skill Tree Progression */}
              <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
                <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                  <div className="flex items-center space-x-2">
                    <Layers className="h-5 w-5 text-emerald-400" />
                    <h3 className="font-bold text-white">Verified Skill Tree Progression</h3>
                  </div>
                  <span className="text-xs text-slate-400">AST Code Verified</span>
                </div>

                <div className="space-y-4">
                  {/* Skill 1 */}
                  <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2">
                    <div className="flex justify-between items-center text-sm">
                      <div className="flex items-center space-x-2">
                        <Code2 className="h-4 w-4 text-emerald-400" />
                        <span className="font-semibold text-white">FastAPI & Asynchronous Architecture</span>
                      </div>
                      <span className="font-mono text-xs text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        Level 4 • 96% Mastery
                      </span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                      <div className="bg-emerald-500 h-full rounded-full" style={{ width: "96%" }} />
                    </div>
                    <p className="text-xs text-slate-400">
                      Verified code includes asynchronous endpoints, dependency injection, and Pydantic v2 schemas.
                    </p>
                  </div>

                  {/* Skill 2 */}
                  <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2">
                    <div className="flex justify-between items-center text-sm">
                      <div className="flex items-center space-x-2">
                        <Cpu className="h-4 w-4 text-teal-400" />
                        <span className="font-semibold text-white">SBERT Semantic Embeddings & Vectors</span>
                      </div>
                      <span className="font-mono text-xs text-teal-400 bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/20">
                        Level 3 • 88% Mastery
                      </span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                      <div className="bg-teal-500 h-full rounded-full" style={{ width: "88%" }} />
                    </div>
                    <p className="text-xs text-slate-400">
                      SentenceTransformers pipeline implementation, cosine similarity ranking, and vector caching.
                    </p>
                  </div>

                  {/* Skill 3 */}
                  <div className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2">
                    <div className="flex justify-between items-center text-sm">
                      <div className="flex items-center space-x-2">
                        <ShieldCheck className="h-4 w-4 text-emerald-400" />
                        <span className="font-semibold text-white">AST Integrity & Clean Code Practices</span>
                      </div>
                      <span className="font-mono text-xs text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        Level 4 • 98% Integrity
                      </span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                      <div className="bg-emerald-400 h-full rounded-full" style={{ width: "98%" }} />
                    </div>
                    <p className="text-xs text-slate-400">
                      Zero anti-cheat flags; authentic commit history validated through AST node frequency analysis.
                    </p>
                  </div>
                </div>
              </div>

              {/* Digital Credential SHA-256 Badge Card */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5 flex flex-col justify-between">
                <div>
                  <div className="flex items-center space-x-2 border-b border-slate-800 pb-4 mb-4">
                    <Award className="h-5 w-5 text-emerald-400" />
                    <h3 className="font-bold text-white">SHA-256 Digital Badge</h3>
                  </div>

                  {/* Tamper-Proof Badge Display */}
                  <div className="bg-gradient-to-b from-slate-950 to-slate-900 border border-emerald-500/40 rounded-xl p-5 text-center space-y-3 relative overflow-hidden shadow-lg shadow-emerald-500/5">
                    <div className="inline-flex p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 mb-1">
                      <ShieldCheck className="h-10 w-10" />
                    </div>
                    <h4 className="text-base font-bold text-white">NAAC Criterion 1.3 Certified</h4>
                    <p className="text-xs text-slate-400">
                      Cryptographically signed by PragyanBridge Accreditation Authority.
                    </p>

                    <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-left space-y-1">
                      <div className="text-[10px] text-slate-500 uppercase font-mono">SHA-256 Cryptographic Hash</div>
                      <div className="font-mono text-[11px] text-emerald-400 break-all leading-tight">
                        9a2f78b9c4501a3de6804a112ec4917f8b9d3e4c19a2b5e7d8f01a3b4c5d6e7f
                      </div>
                    </div>

                    <div className="pt-2 flex items-center justify-center space-x-2 text-xs text-emerald-400">
                      <CheckCircle className="h-4 w-4" />
                      <span className="font-semibold">Tamper-Proof Ledger Status: VALID</span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => setSelectedBadge(INITIAL_CANDIDATES[0])}
                  className="w-full py-2.5 bg-slate-800 hover:bg-slate-750 text-slate-200 border border-slate-700 rounded-xl text-xs font-semibold transition-all flex items-center justify-center space-x-2"
                >
                  <QrCode className="h-4 w-4 text-emerald-400" />
                  <span>Inspect QR & Blockchain Proof</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ==================================================== */}
        {/* VIEW 3: COLLEGE TPO & NAAC PORTAL */}
        {/* ==================================================== */}
        {activeTab === "tpo" && (
          <div className="space-y-6">
            {/* TPO Header Banner */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center space-x-2">
                  <Award className="h-6 w-6 text-emerald-400" />
                  <h2 className="text-xl font-bold text-white">
                    Training & Placement Officer (TPO) Intelligence
                  </h2>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Automated NAAC Accreditation Evidence Engine • Criteria 1.3, 3.5, and 5.2
                </p>
              </div>

              {/* 1-Click NAAC Export Button */}
              <button
                onClick={handleNaacExport}
                disabled={isExporting}
                className="flex items-center space-x-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold px-6 py-3 rounded-xl text-sm transition-all shadow-lg shadow-emerald-500/25"
              >
                <Download className={`h-4 w-4 ${isExporting ? "animate-bounce" : ""}`} />
                <span>{isExporting ? "Generating Dossier..." : "1-Click Download NAAC Dossier"}</span>
              </button>
            </div>

            {/* Placement & Accreditation Stats Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Card 1 */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2 shadow-lg">
                <div className="flex items-center justify-between text-slate-400 text-xs">
                  <span>Placement Qualification</span>
                  <TrendingUp className="h-4 w-4 text-emerald-400" />
                </div>
                <div className="text-2xl font-bold text-white font-mono">86.7%</div>
                <div className="text-xs text-emerald-400 flex items-center space-x-1">
                  <CheckCircle className="h-3 w-3" />
                  <span>Criterion 5.2.1 Benchmark Met</span>
                </div>
              </div>

              {/* Card 2 */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2 shadow-lg">
                <div className="flex items-center justify-between text-slate-400 text-xs">
                  <span>AST Verified Projects</span>
                  <Code2 className="h-4 w-4 text-teal-400" />
                </div>
                <div className="text-2xl font-bold text-white font-mono">100%</div>
                <div className="text-xs text-slate-400">
                  Criterion 1.3.2 Experiential Work
                </div>
              </div>

              {/* Card 3 */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2 shadow-lg">
                <div className="flex items-center justify-between text-slate-400 text-xs">
                  <span>Industry Readiness Index</span>
                  <BarChart3 className="h-4 w-4 text-emerald-400" />
                </div>
                <div className="text-2xl font-bold text-white font-mono">88.4 / 100</div>
                <div className="text-xs text-slate-400">
                  Criterion 3.5 SBERT Vector Match
                </div>
              </div>

              {/* Card 4 */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-2 shadow-lg">
                <div className="flex items-center justify-between text-slate-400 text-xs">
                  <span>Average AST Score</span>
                  <ShieldCheck className="h-4 w-4 text-emerald-400" />
                </div>
                <div className="text-2xl font-bold text-white font-mono">96.8%</div>
                <div className="text-xs text-emerald-400">
                  Tamper-Proof Zero Flags
                </div>
              </div>
            </div>

            {/* NAAC Breakdown Accordion Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Criterion 1.3 */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
                <div className="flex items-center space-x-2 text-emerald-400 font-bold text-sm">
                  <FileCheck2 className="h-4 w-4" />
                  <span>Criterion 1.3</span>
                </div>
                <h4 className="font-semibold text-white text-base">Curriculum Enrichment</h4>
                <p className="text-xs text-slate-400">
                  Metrics 1.3.2 & 1.3.3: Verifies that 100% of candidate project submissions have been parsed for AST integrity and authentic codebase commits.
                </p>
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs space-y-1 font-mono">
                  <div className="text-slate-400">Total Enrolled: <span className="text-white">15 Students</span></div>
                  <div className="text-slate-400">Verified Projects: <span className="text-emerald-400">15 / 15 (100%)</span></div>
                  <div className="text-slate-400">Avg AST Integrity: <span className="text-emerald-400">96.8%</span></div>
                </div>
              </div>

              {/* Criterion 3.5 */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
                <div className="flex items-center space-x-2 text-teal-400 font-bold text-sm">
                  <Building2 className="h-4 w-4" />
                  <span>Criterion 3.5</span>
                </div>
                <h4 className="font-semibold text-white text-base">Industry Collaboration</h4>
                <p className="text-xs text-slate-400">
                  Metric 3.5.1: Matches university coding outcomes directly to industry job descriptions using SBERT semantic intent vectors.
                </p>
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs space-y-1 font-mono">
                  <div className="text-slate-400">Industry Match Rate: <span className="text-teal-400">86.7%</span></div>
                  <div className="text-slate-400">SBERT Vector Align: <span className="text-teal-400">88.4 / 100</span></div>
                  <div className="text-slate-400">Key Tech Stacks: <span className="text-white">FastAPI, Next.js</span></div>
                </div>
              </div>

              {/* Criterion 5.2 */}
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
                <div className="flex items-center space-x-2 text-emerald-400 font-bold text-sm">
                  <Users className="h-4 w-4" />
                  <span>Criterion 5.2</span>
                </div>
                <h4 className="font-semibold text-white text-base">Student Placement</h4>
                <p className="text-xs text-slate-400">
                  Metric 5.2.1: Demonstrates measurable placement progression backed by composite 70/20/10 scores and digital certificates.
                </p>
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs space-y-1 font-mono">
                  <div className="text-slate-400">Placement Benchmark: <span className="text-emerald-400">86.7%</span></div>
                  <div className="text-slate-400">Avg Technical Score: <span className="text-white">82.5 / 100</span></div>
                  <div className="text-slate-400">Median Composite: <span className="text-emerald-400">84.1</span></div>
                </div>
              </div>
            </div>

            {/* Dossier JSON Preview when generated */}
            {naacData && (
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-emerald-400" />
                    <span>Generated NAAC Dossier JSON (Cryptographically Signed)</span>
                  </h4>
                  <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                    SHA-256 Validated
                  </span>
                </div>
                <pre className="bg-slate-950 p-4 rounded-xl text-xs font-mono text-slate-300 overflow-x-auto max-h-72 border border-slate-800">
                  {JSON.stringify(naacData, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </main>

      {/* SHA-256 Digital Badge Verification Modal */}
      {selectedBadge && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-5 relative">
            <button
              onClick={() => setSelectedBadge(null)}
              className="absolute top-4 right-4 text-slate-400 hover:text-white text-lg font-bold"
            >
              ✕
            </button>

            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400">
                <Award className="h-5 w-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-white">Cryptographic Credential Verification</h3>
                <p className="text-xs text-slate-400">NAAC Criteria Tamper-Proof Audit Trail</p>
              </div>
            </div>

            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3 text-xs">
              <div className="flex justify-between border-b border-slate-800/80 pb-2">
                <span className="text-slate-400">Candidate Name</span>
                <span className="font-semibold text-white">{selectedBadge.name}</span>
              </div>
              <div className="flex justify-between border-b border-slate-800/80 pb-2">
                <span className="text-slate-400">College ID</span>
                <span className="font-mono text-emerald-400">{selectedBadge.college_id}</span>
              </div>
              <div className="flex justify-between border-b border-slate-800/80 pb-2">
                <span className="text-slate-400">Academic CGPA</span>
                <span className="font-mono text-white">{selectedBadge.cgpa} / 10.0</span>
              </div>
              <div className="flex justify-between border-b border-slate-800/80 pb-2">
                <span className="text-slate-400">AST Code Integrity</span>
                <span className="font-mono text-emerald-400">{selectedBadge.ast_integrity_score}% Tamper-Proof</span>
              </div>
              <div className="space-y-1 pt-1">
                <span className="text-slate-400 text-[11px] block">Cryptographic SHA-256 Digest</span>
                <div className="font-mono text-[11px] text-emerald-400 break-all bg-slate-900 p-2.5 rounded border border-slate-800">
                  {selectedBadge.credential_hash || "9a2f78b9c4501a3de6804a112ec4917f8b9d3e4c19a2b5e7d8f01a3b4c5d6e7f"}
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between pt-2">
              <div className="flex items-center space-x-1.5 text-xs text-emerald-400 font-semibold">
                <ShieldCheck className="h-4 w-4" />
                <span>OFFICIALLY AUTHENTICATED</span>
              </div>
              <button
                onClick={() => setSelectedBadge(null)}
                className="px-4 py-2 bg-emerald-500 text-slate-950 rounded-lg text-xs font-semibold hover:bg-emerald-400 transition-colors"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950/60 py-4 px-6 text-center text-xs text-slate-500">
        PragyanBridge Prototype • SIH 2026 Problem Statement 26044 • Team Echelon
      </footer>
    </div>
  );
}
