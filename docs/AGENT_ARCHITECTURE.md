# Think9 Pulse: Multi-Agent Intelligence Architecture
**Agentic Consumer Intelligence & Opportunity Engine**

---

## 1. Overview & Agentic Workflow Design

Think9 Pulse deploys a sequential 6-agent pipeline designed to transform fragmented, raw consumer signals into validated, actionable, brand-specific product opportunity proposals.

Unlike single-prompt LLM wrapper patterns, Think9 Pulse enforces strict separation of analytical responsibilities across 6 autonomous specialized agents. Each agent consumes the structured Pydantic output of the preceding agent, executes domain-specific reasoning, enforces schema constraints via Google Gemini API structured output mode (`response_mime_type="application/json"`), and emits an audited, user-safe execution trace.

```
+-----------------------------------------------------------------------------------+
|                            RAW CONSUMER SIGNAL STREAM                             |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 1. SIGNAL COLLECTOR AGENT (agents/signal_collector.py)                             |
| - Cleanses unstructured text from Reddit, Reviews, Search, TikTok & Retail        |
| - Extracts topic, sentiment (-1.0 to 1.0), signal strength (0-1), & key entities  |
+-----------------------------------------------------------------------------------+
                                         │ NormalizedSignal List
                                         ▼
+-----------------------------------------------------------------------------------+
| 2. TREND DETECTION AGENT (agents/trend_detection.py)                               |
| - Clusters normalized signals into macro/micro trend candidates                  |
| - Computes momentum_score (0-100), confidence_score, & growth vectors             |
+-----------------------------------------------------------------------------------+
                                         │ TrendAnalysis
                                         ▼
+-----------------------------------------------------------------------------------+
| 3. CONSUMER INSIGHT AGENT (agents/consumer_insight.py)                             |
| - Formulates Jobs-To-Be-Done (JTBD) framework & consumer problem statements       |
| - Extracts pain points, motivations, barriers, & desired outcomes                 |
+-----------------------------------------------------------------------------------+
                                         │ ConsumerInsight
                                         ▼
+-----------------------------------------------------------------------------------+
| 4. OPPORTUNITY GENERATION AGENT (agents/opportunity_generator.py)                 |
| - Synthesizes insights into concrete product concepts & positioning               |
| - Recommends unique selling propositions (USPs) & key feature specifications      |
+-----------------------------------------------------------------------------------+
                                         │ ProductOpportunity
                                         ▼
+-----------------------------------------------------------------------------------+
| 5. BRAND MATCHING AGENT (agents/brand_matcher.py)                                  |
| - Evaluates opportunity against Think9's 30+ consumer brand portfolio             |
| - Computes multi-dimensional fit scores (strategic, category, audience, capability)|
+-----------------------------------------------------------------------------------+
                                         │ BrandMatchResult
                                         ▼
+-----------------------------------------------------------------------------------+
| 6. RISK / CONFIDENCE VALIDATION AGENT (agents/risk_validator.py)                   |
| - Critical business auditor challenging evidence sufficiency & feasibility        |
| - Computes composite confidence score & assigns status (APPROVED/NEEDS_REVIEW)    |
+-----------------------------------------------------------------------------------+
                                         │ ValidationResult
                                         ▼
+-----------------------------------------------------------------------------------+
|                             VALIDATED OPPORTUNITY CARD                            |
+-----------------------------------------------------------------------------------+
```

---

## 2. Agent Responsibilities & Contracts

### 2.1 BaseAgent Foundation (`agents/base_agent.py`)
- **SDK**: `google-genai` SDK (`genai.Client(api_key=...)`).
- **Configuration**:
  - `model_name`: `"gemini-3.6-flash"` (configurable via `GEMINI_MODEL_NAME`).
  - `temperature`: `0.2` (conservative business intelligence default).
  - `max_output_tokens`: `2048`.
- **Resilience**: Exponential retry mechanism (up to 2 retries) on transient API timeouts or JSON parse errors.
- **Demo Mode**: Controlled fallback mechanism when `GEMINI_API_KEY` is absent or when running offline, explicitly tagged with `"DEMO FALLBACK — NOT GENERATED BY GEMINI"`.

---

### 2.2 Agent 1: Signal Collector (`agents/signal_collector.py`)
- **Role**: Data cleansing and entity normalization.
- **Input**: `List[RawSignal]` (from database).
- **Output Schema**: `SignalCollectorOutput` -> `List[NormalizedSignal]`.
- **Fields**: `original_signal_id`, `topic`, `consumer_need`, `sentiment`, `signal_strength`, `category`, `key_entities`, `rationale`.

---

### 2.3 Agent 2: Trend Detection (`agents/trend_detection.py`)
- **Role**: Signal clustering & velocity pattern recognition.
- **Input**: `SignalCollectorOutput`.
- **Output Schema**: `TrendAnalysis`.
- **Fields**: `trend_name`, `trend_description`, `sector`, `momentum_score`, `confidence_score`, `growth_signal`, `supporting_signal_ids`, `trend_status`.

---

### 2.4 Agent 3: Consumer Insight (`agents/consumer_insight.py`)
- **Role**: Empathic synthesis & Jobs-To-Be-Done (JTBD) framing.
- **Input**: `TrendAnalysis` + `SignalCollectorOutput`.
- **Output Schema**: `ConsumerInsight`.
- **Fields**: `consumer_problem`, `consumer_need`, `target_consumer`, `jobs_to_be_done`, `motivations`, `pain_points`, `barriers`, `desired_outcome`, `supporting_evidence`.

---

### 2.5 Agent 4: Opportunity Generator (`agents/opportunity_generator.py`)
- **Role**: Commercial product concept formulation.
- **Input**: `ConsumerInsight` + `TrendAnalysis`.
- **Output Schema**: `ProductOpportunity`.
- **Fields**: `opportunity_title`, `product_concept`, `product_description`, `target_consumer`, `positioning`, `differentiation`, `suggested_features`, `recommended_next_action`.

---

### 2.6 Agent 5: Brand Matcher (`agents/brand_matcher.py`)
- **Role**: Portfolio alignment & brand fit matrix evaluation.
- **Input**: `ProductOpportunity` + `List[Think9Brand]`.
- **Output Schema**: `BrandMatchResult`.
- **Fields**: `recommended_brand_id`, `recommended_brand_name`, `fit_score` (0-100), `strategic_fit`, `category_fit`, `audience_fit`, `positioning_fit`, `capability_fit`, `rationale`.

---

### 2.7 Agent 6: Risk & Confidence Validator (`agents/risk_validator.py`)
- **Role**: Critical business auditor & risk checker.
- **Input**: `TrendAnalysis` + `ConsumerInsight` + `ProductOpportunity` + `BrandMatchResult`.
- **Output Schema**: `ValidationResult`.
- **Fields**: `overall_confidence`, `evidence_score`, `trend_reliability_score`, `brand_fit_score`, `feasibility_score`, `risk_score`, `identified_risks`, `missing_information`, `validation_status` (`APPROVED` | `NEEDS_REVIEW` | `REJECTED`), `validation_summary`.

---

## 3. Pipeline Orchestration & Traceability

The pipeline orchestrator ([agents/orchestrator.py](file:///Users/abhirupbhowmick/Desktop/think9-pulse/agents/orchestrator.py)) executes all 6 agents sequentially, updating database pipeline run logs and constructing an audit execution trace (`List[AgentExecutionStage]`).

### Execution Trace Record Schema
```json
{
  "stage_name": "5. Brand Portfolio Matching",
  "agent_name": "BrandMatcherAgent",
  "status": "SUCCESS",
  "started_at": "2026-08-10T17:55:00Z",
  "completed_at": "2026-08-10T17:55:01Z",
  "execution_time_ms": 1120,
  "input_summary": "Compared opportunity against 5 Think9 portfolio brands.",
  "output_summary": "Matched opportunity to brand 'NutriPulse' with fit score 95/100.",
  "confidence_score": 95.0
}
```

*Note*: Hidden LLM chain-of-thought scratchpads are never stored or exposed. Only concise, user-safe execution summaries are saved for front-end audit rendering.

---

## 4. API Endpoint Integration

The pipeline is triggered via:

```http
POST /api/v1/pipeline/run?scenario_name=High-Protein%20Breakfast
```

### Sample Response
```json
{
  "pipeline_run_id": "7f1b2c3d-...",
  "scenario": "High-Protein Breakfast",
  "status": "completed",
  "opportunity_id": "8a2b3c4d-...",
  "opportunity_title": "ProBite Savory Protein Egg & Herb Breakfast Squares",
  "matched_brand_name": "NutriPulse",
  "validation_status": "NEEDS_REVIEW",
  "confidence_score": 91.0,
  "summary": "High-confidence opportunity (91%) backed by multi-channel signal consensus...",
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

## 5. Security & Governance

1. **API Key Isolation**: `GEMINI_API_KEY` is loaded strictly on the backend from environment variables.
2. **Schema Safety**: All output payloads are parsed through strict Pydantic v2 schemas before database write operations.
3. **Trace Governance**: Private model prompts and raw secrets are sanitized from logs.
