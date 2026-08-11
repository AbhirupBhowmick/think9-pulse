def test_list_brands(client):
    response = client.get("/api/v1/brands")
    assert response.status_code == 200
    brands = response.json()
    assert isinstance(brands, list)
    assert len(brands) >= 1
    assert brands[0]["name"] == "NutriPulse Test"
    assert brands[0]["sector"] == "Food & Beverage"


def test_get_brand_by_id(client):
    response = client.get("/api/v1/brands")
    brand_id = response.json()[0]["id"]

    detail_response = client.get(f"/api/v1/brands/{brand_id}")
    assert detail_response.status_code == 200
    brand = detail_response.json()
    assert brand["id"] == brand_id
    assert brand["name"] == "NutriPulse Test"


def test_get_brand_not_found(client):
    response = client.get("/api/v1/brands/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
