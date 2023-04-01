ifneq ($(wildcard docker/.env.example),)
	ENV_FILE = .env.example
endif
ifneq ($(wildcard .env.example),)
	ifeq ($(COMPOSE_PROJECT_NAME),)
		include .env.example
	endif
endif
ifneq ($(wildcard docker/.env),)
	ENV_FILE = .env
endif
ifneq ($(wildcard .env),)
	ifeq ($(COMPOSE_PROJECT_NAME),)
		include .env
	endif
endif

export

.PHONY: install
install: ## Installations
	poetry env use python3
	poetry install
	poetry run pre-commit install

.PHONY: run-backend
run-backend: ## Run backend
	uvicorn run:app

.PHONY: migrate-init
migrate-init: ## Initial migrations
	alembic init migrations

.PHONY: migrate-create
migrate-create: ## Create a new revision file
	alembic revision --autogenerate -m "nevers"

.PHONY: migrate-up
migrate-up: ## Upgrade to a later version
	alembic upgrade head

.PHONY: migrate-down
migrate-down: ## Revert to a previous version
	alembic downgrade $(revision)