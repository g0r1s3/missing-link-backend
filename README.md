# Nächste Session (Backend, ~1h)

Ziel: Ein **vollständiges In-Memory CRUD** für `items` mit **Pagination** und **Filter**, sauber in Router/Schemas strukturiert – inkl. kurzer Tests über Swagger/cURL. Das bereitet die spätere DB-Umstellung vor, ohne das API-Interface zu brechen.

---

## Aufgabenplan

1) **Schemas anlegen** (`app/schemas/item.py`)
- `ItemCreate { name, description? }`
- `ItemRead { id, name, description? }`

2) **Router bauen** (`app/api/v1/routers/items.py`)
- `GET /api/v1/items` – `limit`, `offset`, `q` (Filter auf `name`)
- `POST /api/v1/items` – erstellt Item, vergibt `id`
- `GET /api/v1/items/{item_id}` – Detail
- `PUT /api/v1/items/{item_id}` – Update
- `DELETE /api/v1/items/{item_id}` – Delete (204)
- In-Memory „DB“ (Dict) reicht für heute

3) **App verdrahten** (`app/main.py`)
- Router via `app.include_router(items.router, prefix="/api/v1")`
- CORS erlauben: `http://localhost:5173`, `http://localhost:3000`
- App-Meta: `title`, `description`, `version`

4) **Manuelle Tests**
- Server starten: `uvicorn app.main:app --reload`
- Swagger: `http://127.0.0.1:8000/docs`
- cURL Quickchecks:
  ```bash
  curl -s http://127.0.0.1:8000/api/v1/items
  curl -s -X POST http://127.0.0.1:8000/api/v1/items \
    -H "Content-Type: application/json" \
    -d '{"name":"Pumpe","description":"Mini-Handpumpe"}'
  curl -s "http://127.0.0.1:8000/api/v1/items?q=pu&limit=10&offset=0"
  curl -s http://127.0.0.1:8000/api/v1/items/1
  curl -s -X PUT http://127.0.0.1:8000/api/v1/items/1 \
    -H "Content-Type: application/json" \
    -d '{"name":"Pumpe Pro","description":"mit Manometer"}'
  curl -i -X DELETE http://127.0.0.1:8000/api/v1/items/1

