PYTHON := $(shell command -v python3 2> /dev/null || command -v python)

generate:
	$(PYTHON) backend/app/generate_env.py
	sync

up:
	@if [ ! -f .env ]; then make generate; fi
	docker compose up --build

down:
	docker compose down -v

reset:
	docker compose down -v
	docker volume prune -f
	docker system prune -f --volumes
	docker builder prune -f

destroy:
	docker system prune -a --volumes
	@rm -f backend/.env .env