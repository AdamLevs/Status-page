PYTHON := $(shell command -v python3 2> /dev/null || command -v python)

generate:
	$(PYTHON) backend/app/generate_env.py
	sync

up:
	@if [ ! -f .env ]; then make generate; fi
	chmod +x initdb/init.sh
	docker compose up --build

down:
	docker compose down -v

reset:
	docker compose down -v --remove-orphans
	docker volume prune -f
	docker network prune -f
	docker system prune -f --volumes --all

destroy:
	docker system prune -a --volumes
	@rm -f backend/.env .env