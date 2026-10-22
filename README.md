# Dynamic Liquidity Reserve

Synthetic-data treasury decision support. The product is currently at environment/bootstrap stage; the liquidity engine and product workflows are not implemented.

## Local setup

Prerequisites: [uv](https://docs.astral.sh/uv/getting-started/installation/), Python 3.12 (uv can download it), and Docker with Compose for PostgreSQL.

Run commands from the repository root:

```sh
uv sync --locked
cp .env.example .env
docker compose up -d db
uv run --locked uvicorn backend.app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs. Liveness: http://127.0.0.1:8000/health. The health endpoint does not test database connectivity. The DLR-001 contract conventions, demo formats, validation errors, and engineering tradeoffs are documented in [docs/cash-domain-contracts.md](docs/cash-domain-contracts.md).

uv creates `.venv`; activation is optional when using `uv run`. To activate in sh/bash/zsh:

```sh
. .venv/bin/activate
```

## Dependencies

- API: FastAPI, Uvicorn, Pydantic, pydantic-settings, multipart uploads, HTTPX, structlog.
- Persistence: SQLAlchemy 2, Alembic, Psycopg 3 with binary driver and pooling.
- Development: pytest, pytest-asyncio, pytest-cov, Hypothesis, Ruff, mypy, pre-commit.
- Optional retrieval: `uv sync --locked --extra rag` installs pgvector's Python integration. The database image includes the extension; a future migration must enable it. No LLM provider or credentials are configured.

`pyproject.toml` defines direct dependencies; `uv.lock` records exact resolved versions. Commit both files and `.python-version`. Keep `.venv` and `.env` local. Dependency groups follow the [uv project conventions](https://docs.astral.sh/uv/concepts/projects/dependencies/).

```sh
uv add package-name
uv add --dev package-name
uv lock --upgrade-package package-name
uv sync --locked
```

## Quality checks

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy backend
```

Test configuration is ready for tests under `backend/tests`. Once domain tests exist:

```sh
uv run --locked pytest
uv run --locked pytest --cov=backend/app --cov-branch --cov-report=term-missing
```

The documented 90% engine branch-coverage target will apply when the engine exists. Optional Git hooks, after initializing a Git repository: `uv run pre-commit install`.

## Database lifecycle

Apply the tenant-scoped cash-domain schema after PostgreSQL is healthy:

```sh
uv run --locked alembic upgrade head
uv run --locked alembic current
```

`docker compose stop db` stops PostgreSQL while preserving data. `docker compose down` removes the container and preserves the named volume. Local credentials in `.env.example` and Compose are for development only.

## Frontend and scope

The planned React/TypeScript frontend needs Node and its own package manager/lockfile; uv manages Python only. Frontend scaffolding, application migrations, domain features, AI integration, and deployment remain future work. See the specifications in `docs/`.

## Implementation backlog

See [tickets/README.md](tickets/README.md) for concrete implementation tickets, dependencies, acceptance criteria, and the core-versus-optional release plan.
