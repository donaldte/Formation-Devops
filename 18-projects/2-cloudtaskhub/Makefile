# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
SERVICES = gateway auth project billing notification analytics
DOCKER_NAMESPACE ?= cloudtaskhub
DOCKER_USERNAME ?= $(shell echo $$DOCKERHUB_USERNAME)
TAG ?= latest

COMPOSE = docker compose
STACK = docker stack deploy -c docker-compose.yml cloudtaskhub

.PHONY: help
help:
	@echo ""
	@echo "📘 CloudTaskHub Makefile — Version Professionnelle"
	@echo ""
	@echo "Usage : make <command>"
	@echo ""
	@echo "COMMANDES PRINCIPALES :"
	@echo "  make build              → Build docker images (all services)"
	@echo "  make build SERVICE=x    → Build a single service"
	@echo "  make push               → Push images to Docker Hub"
	@echo "  make test               → Run unit tests"
	@echo "  make integration        → Run integration tests with compose"
	@echo "  make deploy             → Deploy stack on Swarm"
	@echo "  make logs               → Show logs of all services"
	@echo "  make rollback TAG=x     → Rollback to a previous tag"
	@echo "  make scan               → Security scan (Trivy)"
	@echo "  make clean              → Cleanup"
	@echo ""


# ===========================================================
# BUILD DOCKER IMAGES (ALL OR ONE)
# ===========================================================
build:
	@for SERVICE in $(SERVICES); do \
		echo "🚀 Building $$SERVICE service..."; \
		docker build -t $(DOCKER_USERNAME)/$(DOCKER_NAMESPACE)-$$SERVICE:$(TAG) \
			./services/$$SERVICE; \
	done

build-one:
	@if [ -z "$(SERVICE)" ]; then \
		echo "❌ Error: SERVICE not specified. Use make build-one SERVICE=gateway"; exit 1; \
	fi
	@echo "🚀 Building $(SERVICE)..."
	docker build -t $(DOCKER_USERNAME)/$(DOCKER_NAMESPACE)-$(SERVICE):$(TAG) \
		./services/$(SERVICE)


# ===========================================================
# PUSH TO DOCKER HUB
# ===========================================================
push:
	@echo "📤 Pushing images to Docker Hub..."
	@for SERVICE in $(SERVICES); do \
		echo "Pushing $$SERVICE..."; \
		docker push $(DOCKER_USERNAME)/$(DOCKER_NAMESPACE)-$$SERVICE:$(TAG); \
	done


# ===========================================================
# TESTS
# ===========================================================
test:
	@echo "🧪 Running unit tests..."
	pytest tests/unit -q

integration:
	@echo "🔄 Running integration tests..."
	$(COMPOSE) -f docker-compose.tests.yml up --build --abort-on-container-exit
	$(COMPOSE) -f docker-compose.tests.yml down -v


# ===========================================================
# DEPLOY SWARM
# ===========================================================
deploy:
	@echo "🚀 Deploying stack with tag $(TAG)..."
	@echo "IMAGE_TAG=$(TAG)" > .env
	$(STACK)


# ===========================================================
# ROLLBACK
# ===========================================================
rollback:
	@if [ -z "$(TAG)" ]; then \
		echo "❌ Error: TAG not specified. Use make rollback TAG=<sha>"; exit 1; \
	fi
	@echo "🔄 Rolling back to tag $(TAG)..."
	@echo "IMAGE_TAG=$(TAG)" > .env
	$(STACK)


# ===========================================================
# LOGS
# ===========================================================
logs:
	@docker service logs -f cloudtaskhub_gateway-service
	@docker service logs -f cloudtaskhub_auth-service
	@docker service logs -f cloudtaskhub_project-service
	@docker service.logs -f cloudtaskhub_billing-service
	@docker service.logs -f cloudtaskhub_notification-service
	@docker service.logs -f cloudtaskhub_analytics-service


# ===========================================================
# SECURITY SCAN (TRIVY)
# ===========================================================
scan:
	@echo "🔍 Scanning Docker images with Trivy..."
	@for SERVICE in $(SERVICES); do \
		echo "Scanning $$SERVICE ..."; \
		trivy image $(DOCKER_USERNAME)/$(DOCKER_NAMESPACE)-$$SERVICE:$(TAG); \
	done


# ===========================================================
# CLEANUP
# ===========================================================
clean:
	@echo "🧹 Cleaning unused Docker images..."
	docker system prune -af
