# Einzeiler für dich: "make up" – startet DB, migriert, seedet, startet API.
.PHONY: up down logs reset db-shell api-shell ps

up:
	@docker compose up -d
	@echo "✔ Backend läuft auf http://localhost:8000  (Docs: http://localhost:8000/docs)"

down:
	@docker compose down

logs:
	@docker compose logs -f --tail=200

reset:
	@docker compose down -v
	@rm -rf ./.docker/pgdata || true
	@docker compose up -d
	@echo "✔ Reset fertig. (Leere DB, Migrationen & Seed laufen automatisch beim API-Start)"

db-shell:
	@docker exec -it ml-postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

api-shell:
	@docker exec -it ml-api bash

ps:
	@docker compose ps
