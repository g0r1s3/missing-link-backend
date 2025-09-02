# app/tests/test_auth_api.py

def register(client, email="alice@example.com", password="secret123"):
    return client.post("/api/v1/auth/register", json={"email": email, "password": password})

def login(client, email="alice@example.com", password="secret123"):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})

def get_token(client, email="alice@example.com", password="secret123"):
    # Nutzer sicherstellen (201 bei neu, 409 falls bereits vorhanden)
    r = register(client, email=email, password=password)
    assert r.status_code in (201, 409)
    r2 = login(client, email=email, password=password)
    assert r2.status_code == 200
    return r2.json()["access_token"]

def test_register_success(client):
    r = register(client, "bob@example.com", "strongPass123")
    assert r.status_code == 201
    data = r.json()
    assert "id" in data and data["email"] == "bob@example.com"

def test_register_duplicate_email(client):
    r1 = register(client, "dup@example.com", "strongPass123")
    assert r1.status_code == 201
    r2 = register(client, "dup@example.com", "strongPass123")
    assert r2.status_code == 409

def test_login_success(client):
    register(client, "carol@example.com", "secret123")
    r = login(client, "carol@example.com", "secret123")
    assert r.status_code == 200
    token = r.json().get("access_token")
    assert token and isinstance(token, str)

def test_login_wrong_password(client):
    register(client, "dave@example.com", "secret123")
    r = login(client, "dave@example.com", "wrongpass1")  # >= 8 Zeichen
    assert r.status_code == 401


def test_protected_create_item_requires_token(client):
    # Ohne Token → 401
    r = client.post("/api/v1/items", json={"name": "Pumpe"})
    assert r.status_code == 401

def test_protected_create_item_with_token(client):
    token = get_token(client, "eve@example.com", "secret123")
    r = client.post(
        "/api/v1/items",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Pumpe", "description": "mit Manometer"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["id"] > 0 and data["name"] == "Pumpe"

def test_public_list_items_is_open(client):
    # Öffentliches GET ohne Token
    r = client.get("/api/v1/items")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_invalid_token_is_rejected(client):
    r = client.post(
        "/api/v1/items",
        headers={"Authorization": "Bearer this.is.not.valid"},
        json={"name": "Foo"},
    )
    assert r.status_code == 401
