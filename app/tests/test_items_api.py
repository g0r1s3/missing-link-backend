# app/tests/test_items_api.py

def _get_token(client, email="test@example.com", password="secret123"):
    client.post("/api/v1/auth/register", json={"email": email, "password": password})
    r = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    return r.json()["access_token"]

def test_create_and_get_via_api(client):
    token = _get_token(client)
    r = client.post(
        "/api/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Pumpe", "description": "Mini"},
    )
    assert r.status_code == 201
    item_id = r.json()["id"]

    r2 = client.get(f"/api/v1/items/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "Pumpe"

def test_list_filter_pagination_api(client):
    token = _get_token(client)
    client.post("/api/v1/items", headers={"Authorization": f"Bearer {token}"}, json={"name": "Pumpe A"})
    client.post("/api/v1/items", headers={"Authorization": f"Bearer {token}"}, json={"name": "Schlauch"})
    client.post("/api/v1/items", headers={"Authorization": f"Bearer {token}"}, json={"name": "Pumpe B"})

    assert len(client.get("/api/v1/items").json()) == 3
    assert len(client.get("/api/v1/items?q=pum").json()) == 2
    assert len(client.get("/api/v1/items?limit=1&offset=0").json()) == 1
    assert len(client.get("/api/v1/items?limit=1&offset=1").json()) == 1

def test_update_and_delete_api(client):
    token = _get_token(client)
    item_id = client.post(
        "/api/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Alt"},
    ).json()["id"]

    r_up = client.put(
        f"/api/v1/items/{item_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Neu"},
    )
    assert r_up.status_code == 200
    assert r_up.json()["name"] == "Neu"

    r_del = client.delete(f"/api/v1/items/{item_id}", headers={"Authorization": f"Bearer {token}"})
    assert r_del.status_code == 204

    assert client.get(f"/api/v1/items/{item_id}").status_code == 404

def test_not_found_paths(client):
    token = _get_token(client)
    # GET bleibt öffentlich → 404 wenn nicht vorhanden
    assert client.get("/api/v1/items/999999").status_code == 404
    # PUT/DELETE sind geschützt → mit Token testen, Route existiert → 404 bei nicht vorhandener ID
    assert client.put("/api/v1/items/999999",
                      headers={"Authorization": f"Bearer {token}"},
                      json={"name": "X"}).status_code == 404
    assert client.delete("/api/v1/items/999999",
                         headers={"Authorization": f"Bearer {token}"}).status_code == 404
