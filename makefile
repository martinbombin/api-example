# Variables
DOCKER_IMAGE=martinbombin/api-example:0.1.0
ENV_CMD=grep -v '^\#' .env | xargs
ENV_TEST_CMD=grep -v '^\#' .env.test | xargs

# Docker Build & Push
build:
	docker build -t $(DOCKER_IMAGE) . -f Dockerfile

push:
	docker push $(DOCKER_IMAGE)

# Docker Compose
up:
	sh -c "$$( $(ENV_CMD) ) docker compose -f docker-compose.yml up --build"

mysql:
	sh -c "$$( $(ENV_CMD) ) docker compose -f docker-compose.yml up --build mysql"

down:
	docker compose down --volumes --remove-orphans

prune:
	docker system prune -f

# Tests
test:
	sh -c "$$( $(ENV_TEST_CMD) ) docker compose -f docker-compose.test.yml up --build"

test-mysql:
	sh -c "$$( $(ENV_TEST_CMD) ) docker compose -f docker-compose.test.yml up --build mysql_integration_tests"

pytest:
	sh -c "$$( $(ENV_TEST_CMD) ) pytest -v"

# Kubernetes
kube-apply:
	kubectl apply -f kubernetes/

kube-forward:
	kubectl port-forward service/app 8000:80