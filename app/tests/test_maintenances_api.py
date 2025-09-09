def get_token_for(client, email="m@test.de", password="supersecret"):
    r = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert r.status_code in (201, 409)
    r2 = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r2.status_code == 200
    return r2.json()["access_token"]

def create_bike(client, token, brand="Canyon"):
    hdr = {"Authorization": f"Bearer {token}"}
    r = client.post("/api/v1/bikes", json={"brand": brand}, headers=hdr)
    assert r.status_code == 201
    return r.json()["id"]

def test_requires_auth(client):
    r = client.post("/api/v1/maintenances", json={})
    assert r.status_code == 401

def test_crud_owner_scoped(client):
    t1 = get_token_for(client, "a@test.de")
    h1 = {"Authorization": f"Bearer {t1}"}
    bike_id = create_bike(client, t1)

    # create
    payload = {
        "bike_id": bike_id,
        "performed_at": "2025-09-09T10:00:00Z",
        "is_external": True,
        "description": "Bremsen justiert",
        "vendor": "BikeShop X",
        "cost": "29.90"
    }
    r = client.post("/api/v1/maintenances", json=payload, headers=h1)
    assert r.status_code == 201
    mid = r.json()["id"]

    # list mine
    r = client.get("/api/v1/maintenances", headers=h1)
    assert r.status_code == 200 and len(r.json()) == 1

    # get
    r = client.get(f"/api/v1/maintenances/{mid}", headers=h1)
    assert r.status_code == 200 and r.json()["vendor"] == "BikeShop X"

    # update
    r = client.put(f"/api/v1/maintenances/{mid}", json={"is_external": False, "vendor": None}, headers=h1)
    assert r.status_code == 200 and r.json()["is_external"] is False

    # other user cannot access
    t2 = get_token_for(client, "b@test.de")
    h2 = {"Authorization": f"Bearer {t2}"}
    assert client.get(f"/api/v1/maintenances/{mid}", headers=h2).status_code == 404
    assert client.put(f"/api/v1/maintenances/{mid}", json={"vendor": "Y"}, headers=h2).status_code == 404
    assert client.delete(f"/api/v1/maintenances/{mid}", headers=h2).status_code == 404

    # delete
    r = client.delete(f"/api/v1/maintenances/{mid}", headers=h1)
    assert r.status_code == 204
