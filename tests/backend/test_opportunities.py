def test_list_opportunities(client):
    response = client.get("/api/v1/opportunities")
    assert response.status_code == 200
    opportunities = response.json()
    assert isinstance(opportunities, list)
    assert len(opportunities) >= 1
    assert opportunities[0]["title"] == "ProBite Test Savory Squares"


def test_get_opportunity_detail(client):
    response = client.get("/api/v1/opportunities")
    opp_id = response.json()[0]["id"]

    detail_response = client.get(f"/api/v1/opportunities/{opp_id}")
    assert detail_response.status_code == 200
    opp = detail_response.json()
    assert opp["id"] == opp_id
    assert opp["confidence_score"] == 92.0
    assert "trend" in opp
    assert "evidence" in opp
    assert len(opp["evidence"]) >= 1


def test_get_opportunity_evidence(client):
    response = client.get("/api/v1/opportunities")
    opp_id = response.json()[0]["id"]

    ev_response = client.get(f"/api/v1/opportunities/{opp_id}/evidence")
    assert ev_response.status_code == 200
    evidence = ev_response.json()
    assert isinstance(evidence, list)
    assert len(evidence) >= 1
    assert evidence[0]["evidence_type"] == "DIRECT_MENTION"
