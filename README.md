# AI-Enabled Skill Intelligence & Personalized Learning Platform

> **Target Ecosystem:** MoSPI / NSSTA / iGOT Karmayogi  
> **Hackathon Track:** Smart India Hackathon (SIH) Government Enterprise Solution

---

## 🏛️ Core Architectural Principle

> *"Deterministic where government decisions need trust. Generative where users need intelligence and flexibility."*

The platform enforces strict separation between decision-making authority and AI assistance:
- **Deterministic Rules Engine:** Calculates required level, assessed level, skill gap, gap severity, and eligibility scores.
- **Recommendation Engine:** Ranks verified courses using a 5-factor weighted scoring model.
- **RAG Engine:** Retrieves grounded competency framework context and role standards.
- **Generative AI (Claude API / Grounded Fallback):** Provides conversational assistance, explains recommendations/gaps, sequences personalized learning paths, and generates structured assessment MCQs.
- **Deterministic Guardrails:** Validates all recommendations against active catalogues and real gaps.

---

## 🌟 Core Unique Features

### 1. Competency Explainability Trail ("Why this course?")
Every course recommendation includes an auditable evidence trail:
```
Learner Profile ➔ Current Level ➔ Required Level ➔ Skill Gap ➔ Course Coverage ➔ Reason
```
Shows transparent score breakdowns across 5 weighted components:
- 40% Competency Gap Match
- 25% Target Role Relevance
- 15% Competency Coverage
- 10% Learner Preference
- 10% Course Quality

### 2. Career / Role Navigator
Allows government officials to select a target role (e.g., *Statistical Officer* ➔ *Senior Statistical Officer*). Displays:
- **Competency Readiness Matrix** (Satisfied vs Priority Gaps)
- **Sequenced Learning Path** (Step 1..N roadmap with prerequisites)
- Uses **"Competency Readiness"** terminology rather than guaranteeing promotion.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ / 20+ / 24+

### 1. Start FastAPI Backend
```bash
cd backend
python -m app.seed
python -m uvicorn main:app --reload --port 8000
```
Backend API docs available at: `http://localhost:8000/docs`

### 2. Start Next.js Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🧪 Running Automated Tests
```bash
cd backend
python -m pytest tests/test_backend.py -v
```

---

## 🛡️ Production Deployment & Security
- Sovereignty: Target deployment on MeghRaj / NIC cloud infrastructure.
- PII Minimization: Redacts personal identifiers before LLM prompts.
- Keycloak: Abstracted authentication interface ready for Keycloak OIDC integration.
