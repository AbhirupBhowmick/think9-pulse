# THINK9 PULSE: Implementation Plan & Challenge Scope

**Project**: Think9 Pulse - Agentic Consumer Intelligence & Opportunity Engine  
**Challenge**: Think9 AI & Intelligence Challenge (Track: Central Consumer Intelligence Engine)  
**Target Deadline**: Production-Ready Prototype Delivery  

---

## 1. Scope Definition & Boundary Strategy

To ensure a high-impact, production-quality prototype delivered within the challenge timeframe, we establish clear boundaries between essential MVP capabilities and out-of-scope features.

### 1.1 In-Scope (MVP Core Capabilities)
- **Representative Data Pipeline**: Simulated consumer signal dataset (Reddit, Amazon Reviews, Search Trends, TikTok Trends, News) covering 5 representative Think9 consumer sectors (F&B, Wellness, Skincare, Athleisure, Home Care).
- **6-Agent Autonomous Workflow**: Full Python pipeline utilizing Gemini API with strict Pydantic JSON response schemas for:
  1. `SignalCollectorAgent`
  2. `TrendDetectionAgent`
  3. `ConsumerInsightAgent`
  4. `OpportunityGenerationAgent`
  5. `BrandMatchingAgent`
  6. `ValidationRiskAgent`
- **Database & Semantic Vector Storage**: PostgreSQL + `pgvector` OR SQLite fallback with vector extensions for local evaluation.
- **FastAPI REST API**: Complete backend supporting opportunity listing, detailed workbench fetching, human approval/rejection actions, trend exploration, brand portfolio management, and on-demand pipeline execution.
- **Executive Frontend Dashboard (Next.js 14 + Tailwind + shadcn/ui)**:
  - Executive Opportunity Overview with KPI statistics.
  - Interactive Opportunity Workbench with deep-dive explainability, signal evidence trace, brand fit breakdown, risk radar chart, and approval controls.
  - Trend Matrix & Category Velocity Explorer.
  - Think9 Brand Portfolio Manager.
  - Real-time Agent Execution & Audit Trail viewer.
- **Pre-loaded Flagship Scenario**: "High-Protein Breakfast" pre-configured with end-to-end evidence trace for instant prototype demonstration.

### 1.2 Out-of-Scope (Explicitly Deferred for Future Phases)
- Live OAuth scraping connectors requiring private social media API keys (X/Twitter, Meta, TikTok APIs).
- Multi-tenant enterprise SSO (SAML/Okta) and fine-grained RBAC permissions.
- Direct automated integration into external ERP / PLM / Supply Chain systems (SAP, NetSuite).
- Heavy offline model fine-tuning; the system relies on Gemini API with structured prompts and semantic embeddings.

---

## 2. Project Directory Structure

```
think9-pulse/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py             # Abstract Base Agent with Gemini API wrapper & prompt formatting
│   ├── signal_collector.py       # SignalCollectorAgent
│   ├── trend_detection.py        # TrendDetectionAgent
│   ├── consumer_insight.py       # ConsumerInsightAgent
│   ├── opportunity_generator.py  # OpportunityGenerationAgent
│   ├── brand_matcher.py          # BrandMatchingAgent
│   └── risk_validator.py         # ValidationRiskAgent
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI entry point & CORS configuration
│   │   ├── config.py             # App environment variables & settings
│   │   ├── database.py           # Database engine & session initialization
│   │   ├── models/               # SQLModel / SQLAlchemy ORM schemas
│   │   │   ├── __init__.py
│   │   │   ├── brand.py
│   │   │   ├── signal.py
│   │   │   ├── trend.py
│   │   │   ├── insight.py
│   │   │   ├── opportunity.py
│   │   │   ├── brand_match.py
│   │   │   ├── risk_validation.py
│   │   │   └── agent_log.py
│   │   ├── schemas/              # Pydantic API Request/Response models
│   │   ├── api/                  # API Routers
│   │   │   ├── opportunities.py
│   │   │   ├── trends.py
│   │   │   ├── brands.py
│   │   │   ├── signals.py
│   │   │   └── pipeline.py
│   │   └── services/             # Pipeline runner & vector search engine
│   │       ├── pipeline_runner.py
│   │       └── vector_store.py
│   └── requirements.txt
├── data/
│   ├── raw_signals.json          # Simulated multi-channel consumer signals dataset
│   ├── think9_brands.json        # Think9 brand portfolio profiles (NutriPulse, GlowBotanica, etc.)
│   └── seed_generator.py         # Script to seed database with initial signals & portfolio
├── database/
│   ├── init.sql                  # PostgreSQL + pgvector schema definition
│   └── migrations/               # Database migration scripts
├── docs/
│   ├── ARCHITECTURE.md           # Technical Architecture Document
│   └── IMPLEMENTATION_PLAN.md    # Phased Implementation Plan
├── frontend/
│   ├── src/
│   │   ├── app/                  # Next.js App Router pages
│   │   │   ├── page.tsx          # Executive Dashboard Overview
│   │   │   ├── opportunities/    # Opportunity List & Detail Workbench
│   │   │   ├── trends/           # Trend Matrix Explorer
│   │   │   ├── brands/           # Brand Portfolio Manager
│   │   │   ├── signals/          # Signal Ingestion Feed
│   │   │   └── pipeline/         # Agent Execution Monitor
│   │   ├── components/           # Reusable UI components & charts
│   │   │   ├── ui/               # shadcn/ui primitives
│   │   │   ├── dashboard/        # KPI cards, opportunity cards, trend radar
│   │   │   ├── workbench/        # Evidence viewer, risk radar, approval panel
│   │   │   └── shared/           # Header, Sidebar, Navigation
│   │   ├── lib/                  # API client, utility functions
│   │   └── types/                # TypeScript interface definitions
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
└── tests/
    ├── backend/                  # pytest suite for API endpoints & database ops
    ├── agents/                   # Unit tests for individual agent structured outputs
    └── frontend/                 # UI component verification tests
```

---

## 3. Phased Implementation Steps

### Phase 1: Foundation & Data Infrastructure
- [ ] Initialize Python backend structure with FastAPI and SQLAlchemy/SQLModel.
- [ ] Implement database schema setup in `database/init.sql` supporting `pgvector`.
- [ ] Create `data/seed_generator.py` and populate `data/think9_brands.json` (5 realistic Think9 brand profiles) and `data/raw_signals.json` (30+ rich consumer signals including the "High-Protein Breakfast" scenario).
- [ ] Validate database connection and seed data ingestion.

### Phase 2: Agent Orchestration Engine & Gemini Contracts
- [ ] Build `agents/base_agent.py` implementing Gemini API calls with `response_mime_type="application/json"` and Pydantic validation.
- [ ] Implement `SignalCollectorAgent` (standardization, sentiment scoring, keyword extraction).
- [ ] Implement `TrendDetectionAgent` (clustering & velocity metrics).
- [ ] Implement `ConsumerInsightAgent` (pain point & JTBD extraction).
- [ ] Implement `OpportunityGenerationAgent` (product concept formulation).
- [ ] Implement `BrandMatchingAgent` (Think9 brand fit matrix & rationale).
- [ ] Implement `ValidationRiskAgent` (multi-factor risk scoring & confidence calculation).
- [ ] Build `backend/app/services/pipeline_runner.py` to coordinate step-by-step agent execution with database state updates and execution logging.

### Phase 3: Backend REST API Development
- [ ] Implement `GET /api/v1/opportunities` (with status, brand, and category filtering).
- [ ] Implement `GET /api/v1/opportunities/{id}` (full opportunity details, evidence, audit logs).
- [ ] Implement `POST /api/v1/opportunities/{id}/approve` & `POST /api/v1/opportunities/{id}/reject`.
- [ ] Implement `GET /api/v1/trends` & `GET /api/v1/brands` & `GET /api/v1/signals`.
- [ ] Implement `POST /api/v1/pipeline/run` (trigger pipeline execution asynchronously).
- [ ] Write backend unit tests in `tests/backend/` and `tests/agents/`.

### Phase 4: Frontend Development (Next.js + Tailwind + shadcn/ui)
- [ ] Initialize Next.js 14 App Router project in `frontend/`.
- [ ] Configure Tailwind CSS, dark-mode color tokens, typography (Inter / Outfit font), and shadcn/ui components.
- [ ] Build Main Layout (Sidebar navigation, Header with pipeline status badge, quick search).
- [ ] Build **Executive Dashboard Overview** (`/`):
  - High-level KPI cards (Total Opportunities, Active Trends, High-Confidence Proposals, Approved Brands).
  - Top Opportunities Carousel / Grid.
  - Trend Velocity Heatmap.
- [ ] Build **Opportunity Feed & Workbench** (`/opportunities` & `/opportunities/[id]`):
  - Filterable Grid / Table view.
  - Comprehensive Workbench view featuring:
    - Opportunity Card Header (Status tag, Confidence Score gauge, Brand badge).
    - Concept Summary & Target Positioning.
    - Signal Evidence Trace (clickable raw signals, source type, sentiment).
    - Brand Match Analysis (fit score, strategic alignment, alternative brands).
    - Risk Radar & Breakdown Chart (Recharts radar chart).
    - Agent Reasoning Audit Trail (expandable step-by-step agent thoughts).
    - Human Approval Control Bar (Approve, Reject, Request Revision with notes).
- [ ] Build **Trend Matrix View** (`/trends`), **Brand Portfolio Manager** (`/brands`), **Signal Feed** (`/signals`), and **Agent Execution Monitor** (`/pipeline`).

### Phase 5: Verification, Seeding & Polish
- [ ] Run full end-to-end pipeline test on the "High-Protein Breakfast" scenario.
- [ ] Verify UI responsiveness, animations, light/dark mode polish, and empty/loading state handling.
- [ ] Confirm zero API key leakage in browser client bundles.
- [ ] Create walkthrough documentation and verify all API endpoints return clean structured JSON responses.

---

## 4. Verification Plan

### 4.1 Automated Testing
- **Backend APIs**: `pytest backend/tests` verifying all REST endpoints return proper status codes and Pydantic schemas.
- **Agents**: Direct invocation tests ensuring Gemini API returns strictly conforming JSON output matching agent Pydantic contracts.

### 4.2 Manual & Visual Verification
- **End-to-End Workflow**: Trigger pipeline run via API/UI and verify opportunity progression from Raw Signal -> Approved Opportunity.
- **Deep-Dive Explainability**: Verify every generated opportunity in `/opportunities/[id]` lists clickable evidence signals and complete step-by-step agent logs.
- **Human Approval Action**: Click "Approve", verify database update to `APPROVED`, and verify UI state update in real time.
