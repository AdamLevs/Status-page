PYTHON := $(shell command -v python3 2> /dev/null || command -v python)

generate:
	$(PYTHON) app/generate_env.py
	sync

up:
	@if [ ! -f .env ]; then make generate; fi
	sleep 1
	docker compose up --build

down:
	docker compose down -v

hard-reset:
	docker compose down -v
	docker volume prune -f
	docker system prune -f --volumes
	docker builder prune -f