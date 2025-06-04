# Makefile for managing the Dockerized application environment - added by [name of the author] and then modified by the commends of the user
PYTHON := $(shell command -v python3 2> /dev/null || command -v python)

# generate environment variables
generate:
	$(PYTHON) backend/app/generate_env.py
	sync

# run the application
up:
	@if [ ! -f .env ]; then make generate; fi
	chmod +x initdb/init.sh
	docker compose up --build

# shut down the application
down:
	docker compose down -v
	@rm -f backend/.env .env

# make a full reset of the application
reset:
	docker compose down -v --remove-orphans
	docker volume prune -f
	docker network prune -f
	docker system prune -f --volumes --all

# MAKE A FULL RESET TO DOCKER VOLUMES! USE WITH CAUTION!
destroy:
	docker system prune -a --volumes
	@rm -f backend/.env .env