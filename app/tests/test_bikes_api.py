from fastapi.testclient import TestClient


# app/tests/test_bikes_api.py
def get_token_for(
    client: TestClient, email: str = "a@test.de", password: str = "supersecret"
) -> str:
    r = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert r.status_code in (201, 409)
    r2 = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert r2.status_code == 200
    return r2.json()["access_token"]


def test_bike_crud_requires_auth(client: TestClient) -> None:
    r = client.post("/api/v1/bikes", json={"brand": "Canyon"})
    assert r.status_code == 401


# ... existing code ...


def test_bike_crud_happy_path(client: TestClient) -> None:
    token = get_token_for(client)
    hdr = {"Authorization": f"Bearer {token}"}

    r = client.post(
        "/api/v1/bikes", json={"brand": "Canyon", "model": "Endurace", "year": 2022}, headers=hdr
    )
    assert r.status_code == 201
    bike = r.json()
    bike_id = bike["id"]

    r = client.get("/api/v1/bikes", headers=hdr)
    assert r.status_code == 200 and len(r.json()) == 1

    r = client.get(f"/api/v1/bikes/{bike_id}", headers=hdr)
    assert r.status_code == 200 and r.json()["model"] == "Endurace"

    r = client.put(f"/api/v1/bikes/{bike_id}", json={"color": "schwarz"}, headers=hdr)
    assert r.status_code == 200 and r.json()["color"] == "schwarz"

    r = client.delete(f"/api/v1/bikes/{bike_id}", headers=hdr)
    assert r.status_code == 204

    r = client.get(f"/api/v1/bikes/{bike_id}", headers=hdr)
    assert r.status_code == 404


# ... existing code ...


def test_bike_is_owner_scoped(client: TestClient) -> None:
    token_a = get_token_for(client, email="a@test.de")
    hdr_a = {"Authorization": f"Bearer {token_a}"}
    bike_id = client.post("/api/v1/bikes", json={"brand": "Canyon"}, headers=hdr_a).json()["id"]

    token_b = get_token_for(client, email="b@test.de")
    hdr_b = {"Authorization": f"Bearer {token_b}"}

    assert client.get(f"/api/v1/bikes/{bike_id}", headers=hdr_b).status_code == 404
    assert (
        client.put(f"/api/v1/bikes/{bike_id}", json={"brand": "X"}, headers=hdr_b).status_code
        == 404
    )
    assert client.delete(f"/api/v1/bikes/{bike_id}", headers=hdr_b).status_code == 404
