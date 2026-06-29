# campofacil-be

FastAPI backend for Campo Fácil.

## Stack

- **Python 3.11+** with FastAPI
- **PostgreSQL 17** (via Docker)
- **Keycloak 26** for authentication (via Docker)
- **SQLAlchemy** ORM + **Alembic** migrations

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/)
- Docker + Docker Compose

## Setup

**1. Start infrastructure**

```bash
docker compose up -d
```

This starts PostgreSQL on port `5555` and Keycloak on port `8888`. Keycloak is auto-configured with a `campofacil` realm and client on first start.

**2. Configure environment**

Key variables:

| Variable        | Default                                                    | Description           |
| --------------- | ---------------------------------------------------------- | --------------------- |
| `DATABASE_URL`  | `postgresql://postgres:postgres@localhost:5555/campofacil` | PostgreSQL connection |
| `AUTH_PROVIDER` | `keycloak`                                                 | `keycloak`            |
| `KEYCLOAK_URL`  | `http://localhost:8888`                                    | Keycloak base URL     |

**3. Install dependencies**

```bash
python -m venv venv
source venv/bin/activate
pip install poetry
poetry install
```

**4. Apply database migrations**

```bash
poetry run alembic upgrade head
```

**5. Run the development server**

```bash
poetry run fastapi dev main.py
```

API available at http://localhost:8000  
Interactive docs at http://localhost:8000/docs

## Database migrations

All commands run from `campofacil-be/`. Alembic reads `DATABASE_URL` from `.env` automatically.

```bash
# Apply all pending migrations
poetry run alembic upgrade head

# Create a migration after changing a model
poetry run alembic revision --autogenerate -m "short description"

# Roll back one migration
poetry run alembic downgrade -1

# Check current state
poetry run alembic current
poetry run alembic history
```

> After creating a new SQLAlchemy model, import it in `src/campofacil_be/models/__init__.py` before running autogenerate.
