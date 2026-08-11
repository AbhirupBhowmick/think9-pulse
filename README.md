# THINK9 PULSE

**Central Consumer Intelligence & Opportunity Engine for Think9 Portfolio Brands**

THINK9 PULSE is an agentic AI consumer intelligence platform designed to convert raw consumer signals into evidence-backed, commercial product opportunities tailored for Think9 portfolio brands.

The platform takes a user's consumer/market research question and orchestrates a 6-stage reasoning pipeline powered by **Gemini 3.6 Flash** (`gemini-3.6-flash`).

---

## 🌟 Key Features & Philosophy

### 1. User-Directed Analysis
- Users enter any consumer intelligence or market demand question (e.g., *"Find unmet demand for quick healthy breakfast products"*).
- The pipeline investigates available internal consumer signals in direct context of the question.

### 2. 6-Stage Specialized Agentic Architecture
The engine executes a sequential 6-agent workflow:
1. **Understand the Consumer** (`SignalCollectorAgent`): Ingests and normalizes multi-channel consumer signals.
2. **Find Emerging Trends** (`TrendDetectionAgent`): Clusters normalized signals into emerging category trends with momentum and confidence scoring.
3. **Understand What People Need** (`ConsumerInsightAgent`): Formulates Jobs-To-Be-Done (JTBD) frameworks and identifies core pain points.
4. **Suggest a Product Opportunity** (`OpportunityGeneratorAgent`): Translates insights into actionable product concepts.
5. **Find the Best Brand Fit** (`BrandMatcherAgent`): Matches product concepts against Think9 portfolio brands (*NutriPulse*, *GlowBotanica*, *AuraFlex*, *PureHabit*, *VitalHydrate*).
6. **Check Confidence & Risks** (`RiskValidatorAgent`): Audits evidence sufficiency, market risks, regulatory factors, and composite confidence score.

### 3. Human Checkpoint Philosophy
- **AI Recommends. A Human Makes the Final Business Decision.**
- Opportunities requiring further validation are flagged as `NEEDS_REVIEW` to ensure human oversight before commercial execution.

### 4. Data Source Scope
- **Internal / Stored Consumer Signals**: Ingests pre-indexed consumer signals stored within the system database (multi-channel representative signals from search spikes, review feedback, community threads, and video analytics).
- *Note*: Live external API crawling (e.g., real-time social scraping) is not active; all analyses run strictly against internal stored signal data.

---

## 🛠️ Technology Stack

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: Python 3.14, FastAPI, Uvicorn, SQLAlchemy, Pydantic v2
- **AI Orchestration**: Google GenAI SDK (`google-genai`), Gemini 3.6 Flash (`gemini-3.6-flash`), Pydantic Structured Outputs
- **Database**: SQLite

---

## 🚀 Local Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env` based on `.env.example`:

```env
APP_ENV=development
PROJECT_NAME="Think9 Pulse API"
API_V1_STR=/api/v1
DATABASE_URL=sqlite:///../think9_pulse.db
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Google Gemini API Settings
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
GEMINI_MODEL_NAME=gemini-3.6-flash
DEMO_MODE=false
```

Seed the database and start the FastAPI server:

```bash
# Seed initial signals & brands
python -m app.db.init_db

# Start uvicorn server
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🔒 Security & Environment Variables

The following environment variables are required for running the application locally:
- `GEMINI_API_KEY`: Your Google AI Studio API Key.
- `GEMINI_MODEL_NAME`: Set to `gemini-3.6-flash`.
- `DATABASE_URL`: Path to the local SQLite database.

*All API keys and local `.env` files are strictly excluded from version control.*
