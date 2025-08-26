def test_create_and_get_via_api(client):
    # Create
    r = client.post("/api/v1/items", json={"name": "Pumpe", "description": "Mini"})
    assert r.status_code == 201
    data = r.json()
    assert data["id"] > 0
    assert data["name"] == "Pumpe"

    # Read
    item_id = data["id"]
    r2 = client.get(f"/api/v1/items/{item_id}")
    assert r2.status_code == 200
    assert r2.json()["name"] == "Pumpe"

def test_list_filter_pagination_api(client):
    client.post("/api/v1/items", json={"name": "Pumpe A"})
    client.post("/api/v1/items", json={"name": "Schlauch"})
    client.post("/api/v1/items", json={"name": "Pumpe B"})

    # List all
    r_all = client.get("/api/v1/items")
    assert r_all.status_code == 200
    assert len(r_all.json()) == 3

    # Filter q
    r_q = client.get("/api/v1/items?q=pum")
    assert r_q.status_code == 200
    assert len(r_q.json()) == 2

    # Pagination
    r_page1 = client.get("/api/v1/items?limit=1&offset=0")
    r_page2 = client.get("/api/v1/items?limit=1&offset=1")
    assert len(r_page1.json()) == 1
    assert len(r_page2.json()) == 1

def test_update_and_delete_api(client):
    # create
    r = client.post("/api/v1/items", json={"name": "Alt"})
    item_id = r.json()["id"]

    # update
    r_up = client.put(f"/api/v1/items/{item_id}", json={"name": "Neu"})
    assert r_up.status_code == 200
    assert r_up.json()["name"] == "Neu"

    # delete
    r_del = client.delete(f"/api/v1/items/{item_id}")
    assert r_del.status_code == 204

    # 404 after delete
    r_get = client.get(f"/api/v1/items/{item_id}")
    assert r_get.status_code == 404

def test_not_found_paths(client):
    assert client.get("/api/v1/items/999999").status_code == 404
    assert client.put("/api/v1/items/999999", json={"name": "X"}).status_code == 404
    assert client.delete("/api/v1/items/999999").status_code == 404
