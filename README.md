# Api Example

This is a technical test project built using **FastAPI**, **MySQL**, **Docker**, and **Kubernetes**. It provides a simple user management API with tests.

---

## 🚀 Tech Stack

- Python 3.13+
- [FastAPI](https://fastapi.tiangolo.com/)
- SQLAlchemy
- MySQL
- Docker & Docker Compose
- Kubernetes
- Pytest
- Poetry

---

## 📦 Local Development

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/api-example.git
cd api-example
```

### 2. Set up the environment

Create a .env file with necessary environment variables (see .env.template).

### 3. Run the app

```bash
make up
```

### 4. Tear down (with cleanup)

```bash
make down
make prune
```

## 🐳 Docker

### Build and Push Image

```bash
make build
make push
```

## 🧪 Running Tests

### Using Docker Compose

```bash
make test
```

Or run specific services like test DB and then pytest:

```bash
make test-mysql
make pytest
```

## ☁️ Kubernetes Deployment

Ensure your Kubernetes cluster is running and kubectl is configured.

```bash
make kube-apply
```

And forward the service to use it.

```bash
make kube-forward
```

## 📖 API Documentation

FastAPI automatically provides interactive documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧱 Project Structure

<pre><code>.
├── app/
│   ├── main.py              # FastAPI app entrypoint
│   ├── models.py            # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   ├── repositories/        # DB access
│   ├── routers/             # API routes
│   ├── config.py            # App config
│   └── exceptions.py        # Custom exceptions
├── tests/                   # Unit & integration tests
├── kubernetes/              # K8s manifests
├── Dockerfile
├── docker-compose.yml
├── Dockerfile_test
├── docker-compose.test.yml
├── pyproject.toml
└── README.md
</code></pre>