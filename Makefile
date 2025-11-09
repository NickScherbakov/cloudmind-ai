# CloudMind AI Makefile
# Convenient commands for Docker-based development

.PHONY: help setup build up dev test stop clean logs shell lint

# Docker Compose command (supports both V1 and V2)
DOCKER_COMPOSE := $(shell if docker compose version > /dev/null 2>&1; then echo "docker compose"; else echo "docker-compose"; fi)

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "CloudMind AI - Docker Commands"
	@echo "=============================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Initial setup - create .env and credentials directory
	@echo "Setting up CloudMind AI..."
	@if [ ! -f .env ]; then cp .env.example .env && echo "✓ Created .env file"; fi
	@mkdir -p credentials && echo "✓ Created credentials directory"
	@echo "✓ Setup complete!"

build: ## Build Docker images
	@echo "Building Docker images..."
	$(DOCKER_COMPOSE) build
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml build

up: ## Start in production mode
	@echo "Starting CloudMind AI (production mode)..."
	$(DOCKER_COMPOSE) up -d
	@echo "✓ CloudMind AI is running at http://localhost:8000"

dev: ## Start in development mode with hot-reload
	@echo "Starting CloudMind AI (development mode)..."
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml up

test: ## Run tests in Docker container
	@echo "Running tests..."
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml run --rm cloudmind-test

stop: ## Stop all services
	@echo "Stopping services..."
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml down

clean: ## Remove all containers, images, and volumes
	@echo "Cleaning up..."
	$(DOCKER_COMPOSE) down -v --rmi local
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml down -v --rmi local
	@echo "✓ Cleanup complete"

logs: ## Show logs from running containers
	$(DOCKER_COMPOSE) logs -f

logs-dev: ## Show logs from development containers
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml logs -f

shell: ## Open shell in development container
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml run --rm cloudmind-dev /bin/bash

shell-prod: ## Open shell in production container
	$(DOCKER_COMPOSE) run --rm cloudmind-api /bin/bash

ps: ## Show running containers
	$(DOCKER_COMPOSE) ps
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml ps

restart: ## Restart services
	$(DOCKER_COMPOSE) restart
	$(DOCKER_COMPOSE) -f docker-compose.dev.yml restart

# Local development without Docker
install: ## Install dependencies locally (without Docker)
	pip install -r requirements.txt

run-local: ## Run API locally (without Docker)
	PYTHONPATH=src python cloudmind_api.py

test-local: ## Run tests locally (without Docker)
	PYTHONPATH=src pytest tests/ -v

cli: ## Run CLI locally (without Docker)
	PYTHONPATH=src python cloudmind_cli.py $(ARGS)
