# campofacil-api

REST API for Campo Fácil — manages clients and products with Keycloak-based authentication.

## Stack

- **Python 3.11+** with FastAPI
- **PostgreSQL 17** with pgvector (via Docker)
- **Keycloak 26** for authentication (via Docker)
- **SQLAlchemy** ORM + **Alembic** migrations

## Repository layout

```
campofacil-api/
├── app/                  # FastAPI application
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── routes/           # Route handlers
│   └── alembic/          # Database migrations
├── scripts/
│   └── keycloak/         # Keycloak realm bootstrap script
└── docker-compose.yaml   # PostgreSQL + Keycloak services
```

## Quick start

**1. Start infrastructure**

```bash
docker compose up -d
```

Starts PostgreSQL on port `5555` and Keycloak on port `8888`. The `campofacil-configuration` container bootstraps the Keycloak realm and client automatically.

**2. Run the API**

See [app/README.md](app/README.md) for the full setup guide.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/token` | Exchange username/password for a Bearer token |
| GET | `/clients/` | List clients |
| POST | `/clients/` | Create a client |
| GET | `/clients/{id}` | Get a client |
| PUT | `/clients/{id}` | Update a client |
| DELETE | `/clients/{id}` | Delete a client |
| GET | `/products/` | List products |
| POST | `/products/` | Create a product |
| GET | `/products/{id}` | Get a product |
| PUT | `/products/{id}` | Update a product |
| DELETE | `/products/{id}` | Delete a product |

All endpoints except `POST /auth/token` require `Authorization: Bearer <token>`.

Interactive docs available at http://localhost:8000/docs once the API is running.
