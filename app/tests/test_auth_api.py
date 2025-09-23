from fastapi.testclient import TestClient


# app/tests/test_auth_api.py
def test_register_and_login_and_protected(client: TestClient) -> None:
    # register
    r = client.post("/api/v1/auth/register", json={"email": "a@test.de", "password": "supersecret"})
    assert r.status_code == 201

    # duplicate -> 409
    r_dup = client.post(
        "/api/v1/auth/register", json={"email": "a@test.de", "password": "supersecret"}
    )
    assert r_dup.status_code == 409

    # login
    r_login = client.post(
        "/api/v1/auth/login", json={"email": "a@test.de", "password": "supersecret"}
    )
    assert r_login.status_code == 200
    token = r_login.json()["access_token"]

    # protected: create item
    r_no = client.post("/api/v1/items", json={"name": "X"})  # ohne Token
    assert r_no.status_code == 401

    r_ok = client.post(
        "/api/v1/items",
        json={"name": "X"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r_ok.status_code == 201
