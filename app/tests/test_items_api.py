def test_create_and_get_via_api(client):
    r = client.post("/api/v1/items", json={"name": "Pumpe", "description": "Mini"})
    assert r.status_code == 201
    data = r.json()
    item_id = data["id"]

    r2 = client.get(f"/api/v1/items/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "Pumpe"

def test_list_filter_pagination_api(client):
    client.post("/api/v1/items", json={"name": "Pumpe A"})
    client.post("/api/v1/items", json={"name": "Schlauch"})
    client.post("/api/v1/items", json={"name": "Pumpe B"})

    assert len(client.get("/api/v1/items").json()) == 3
    assert len(client.get("/api/v1/items?q=pum").json()) == 2
    assert len(client.get("/api/v1/items?limit=1&offset=0").json()) == 1
    assert len(client.get("/api/v1/items?limit=1&offset=1").json()) == 1

def test_update_and_delete_api(client):
    item_id = client.post("/api/v1/items", json={"name": "Alt"}).json()["id"]
    assert client.put(f"/api/v1/items/{item_id}", json={"name": "Neu"}).status_code == 200
    assert client.delete(f"/api/v1/items/{item_id}").status_code == 204
    assert client.get(f"/api/v1/items/{item_id}").status_code == 404

def test_not_found_paths(client):
    assert client.get("/api/v1/items/999999").status_code == 404
    assert client.put("/api/v1/items/999999", json={"name": "X"}).status_code == 404
    assert client.delete("/api/v1/items/999999").status_code == 404
