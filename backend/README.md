# Think9 Pulse - Backend & Agent Intelligence Engine

Backend REST API & Multi-Agent Intelligence Engine for **THINK9 PULSE**: Agentic Consumer Intelligence & Opportunity Engine.

---

## Prerequisites
- **Python**: 3.11 or 3.12+
- **Google GenAI SDK**: `google-genai` (included in `requirements.txt`)
- **Database**: PostgreSQL 15+ with `pgvector` extension (or SQLite for local development/testing).

---

## Setup & Environment Installation

### 1. Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Set environment variables:
```env
APP_ENV=development
PROJECT_NAME="Think9 Pulse API"
API_V1_STR=/api/v1
DATABASE_URL=sqlite:///./think9_pulse.db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Google Gemini API Settings
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL_NAME=gemini-3.6-flash
GEMINI_TEMPERATURE=0.2

# Demo Mode Configuration
DEMO_MODE=true
```

---

## Multi-Agent Intelligence Suite

Think9 Pulse features a 6-agent sequential pipeline:

1. **Signal Collector Agent** (`SignalCollectorAgent`): Ingests & normalizes multi-channel signals.
2. **Trend Detection Agent** (`TrendDetectionAgent`): Clusters signals into trend candidates & momentum metrics.
3. **Consumer Insight Agent** (`ConsumerInsightAgent`): Formulates JTBD frameworks & pain point synthesis.
4. **Opportunity Generation Agent** (`OpportunityGeneratorAgent`): Translates insights into product concepts.
5. **Brand Matching Agent** (`BrandMatcherAgent`): Evaluates concept fit against Think9's portfolio brands.
6. **Risk / Confidence Validation Agent** (`RiskValidatorAgent`): Audits evidence sufficiency & commercial risks.

---

## Database Seeding

Populate the database with representative Think9 consumer brand profiles, signals, trends, and the flagship **"High-Protein Breakfast"** opportunity:

```bash
python ../data/seed_generator.py
```

---

## Running the API Server

Launch the Uvicorn development server:

```bash
uvicorn app.main:app --reload --port 8000
```

---

## Executing the Agentic Pipeline API

### Triggering a Pipeline Run

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/pipeline/run?scenario_name=High-Protein%20Breakfast"
```

### Example Pipeline Response

```json
{
  "pipeline_run_id": "8f3b2a1c-...",
  "scenario": "High-Protein Breakfast",
  "status": "completed",
  "opportunity_id": "9a4b2c1d-...",
  "opportunity_title": "ProBite Savory Protein Egg & Herb Breakfast Squares",
  "matched_brand_name": "NutriPulse",
  "validation_status": "NEEDS_REVIEW",
  "confidence_score": 91.0,
  "summary": "High-confidence opportunity (91%) backed by multi-channel signal consensus.",
  "execution_stages": [
    { "stage_name": "1. Signal Collection", "status": "SUCCESS", "execution_time_ms": 420 },
    { "stage_name": "2. Trend Detection", "status": "SUCCESS", "execution_time_ms": 580 },
    { "stage_name": "3. Consumer Insight Synthesis", "status": "SUCCESS", "execution_time_ms": 610 },
    { "stage_name": "4. Opportunity Generation", "status": "SUCCESS", "execution_time_ms": 750 },
    { "stage_name": "5. Brand Portfolio Matching", "status": "SUCCESS", "execution_time_ms": 490 },
    { "stage_name": "6. Risk & Confidence Audit", "status": "SUCCESS", "execution_time_ms": 810 }
  ]
}
```

---

## Running Automated Tests

Run the complete Phase 1 + Phase 2 test suite:

```bash
pytest ../tests/backend
```

All 20 backend and agent tests use mocked Gemini fixtures to run offline cleanly without consuming live Gemini API credits.
