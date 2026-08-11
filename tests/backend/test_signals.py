def test_list_signals(client):
    response = client.get("/api/v1/signals")
    assert response.status_code == 200
    signals = response.json()
    assert isinstance(signals, list)
    assert len(signals) >= 1
    assert signals[0]["source"] == "Reddit"


def test_get_signal_by_id(client):
    response = client.get("/api/v1/signals")
    signal_id = response.json()[0]["id"]

    detail_response = client.get(f"/api/v1/signals/{signal_id}")
    assert detail_response.status_code == 200
    signal = detail_response.json()
    assert signal["id"] == signal_id
    assert signal["sector"] == "Food & Beverage"


def test_get_signal_not_found(client):
    response = client.get("/api/v1/signals/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
