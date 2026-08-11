"""
Verification script for Think9 Pulse FastAPI endpoints.
Tests all GET routes against the seeded database.
"""

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
backend_dir = os.path.join(project_root, "backend")
sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def verify_all():
    print("🔍 Verifying Think9 Pulse REST API Endpoints...\n")

    # 1. Health
    res = client.get("/api/v1/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print(f"✅ GET /api/v1/health -> {res.json()}")

    # 2. Brands
    res = client.get("/api/v1/brands")
    assert res.status_code == 200
    brands = res.json()
    assert len(brands) == 5, f"Expected 5 brands, got {len(brands)}"
    print(f"✅ GET /api/v1/brands -> Found {len(brands)} Think9 brands (First: {brands[0]['name']})")

    brand_id = brands[0]["id"]
    res_b = client.get(f"/api/v1/brands/{brand_id}")
    assert res_b.status_code == 200
    print(f"✅ GET /api/v1/brands/{brand_id} -> {res_b.json()['name']}")

    # 3. Signals
    res = client.get("/api/v1/signals")
    assert res.status_code == 200
    signals = res.json()
    assert len(signals) == 6, f"Expected 6 signals, got {len(signals)}"
    print(f"✅ GET /api/v1/signals -> Found {len(signals)} consumer signals (First source: {signals[0]['source']})")

    signal_id = signals[0]["id"]
    res_s = client.get(f"/api/v1/signals/{signal_id}")
    assert res_s.status_code == 200
    print(f"✅ GET /api/v1/signals/{signal_id} -> Title: {res_s.json().get('title')}")

    # 4. Trends
    res = client.get("/api/v1/trends")
    assert res.status_code == 200
    trends = res.json()
    assert len(trends) >= 1
    print(f"✅ GET /api/v1/trends -> Found {len(trends)} trend (Name: '{trends[0]['name']}', Momentum: {trends[0]['momentum_score']})")

    trend_id = trends[0]["id"]
    res_t = client.get(f"/api/v1/trends/{trend_id}")
    assert res_t.status_code == 200
    print(f"✅ GET /api/v1/trends/{trend_id} -> {res_t.json()['name']}")

    # 5. Opportunities
    res = client.get("/api/v1/opportunities")
    assert res.status_code == 200
    opps = res.json()
    assert len(opps) >= 1
    print(f"✅ GET /api/v1/opportunities -> Found {len(opps)} opportunity (Title: '{opps[0]['title']}', Confidence: {opps[0]['confidence_score']}%)")

    opp_id = opps[0]["id"]
    res_o = client.get(f"/api/v1/opportunities/{opp_id}")
    assert res_o.status_code == 200
    opp_detail = res_o.json()
    assert "evidence" in opp_detail and len(opp_detail["evidence"]) == 5
    print(f"✅ GET /api/v1/opportunities/{opp_id} -> Detail loaded with {len(opp_detail['evidence'])} evidence signals")

    # 6. Opportunity Evidence
    res_ev = client.get(f"/api/v1/opportunities/{opp_id}/evidence")
    assert res_ev.status_code == 200
    evs = res_ev.json()
    assert len(evs) == 5
    print(f"✅ GET /api/v1/opportunities/{opp_id}/evidence -> Returned {len(evs)} evidence records")

    # 7. Pipeline Runs
    res = client.get("/api/v1/pipeline/runs")
    assert res.status_code == 200
    runs = res.json()
    assert len(runs) >= 1
    print(f"✅ GET /api/v1/pipeline/runs -> Found {len(runs)} run log (Scenario: '{runs[0]['scenario_name']}', Status: '{runs[0]['status']}')")

    run_id = runs[0]["id"]
    res_r = client.get(f"/api/v1/pipeline/runs/{run_id}")
    assert res_r.status_code == 200

    # 8. Pipeline Trigger POST (Real Agentic Multi-Agent Execution)
    res_trig = client.post("/api/v1/pipeline/run?scenario_name=High-Protein%20Breakfast")
    assert res_trig.status_code == 200, f"Pipeline execution failed: {res_trig.text}"
    trig_data = res_trig.json()
    assert trig_data["status"] == "completed"
    assert len(trig_data["execution_stages"]) == 6
    print(f"✅ POST /api/v1/pipeline/run -> Executed all 6 agents successfully! Opportunity: '{trig_data['opportunity_title']}' (Confidence: {trig_data['confidence_score']}%, Status: {trig_data['validation_status']})")

    print("\n🎉 ALL BACKEND & AGENT SUITE ENDPOINTS VERIFIED SUCCESSFULLY!")


if __name__ == "__main__":
    verify_all()
