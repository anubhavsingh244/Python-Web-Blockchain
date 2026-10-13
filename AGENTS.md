# AGENTS.md

Flask "Web Based Blockchain" demo. Sandbox/dev environment is defined in
`docker-compose.base44.yml` — use that, not the repo's own `docker-compose.yml`.

## Run it

```bash
docker compose -f docker-compose.base44.yml up -d --build
curl -s http://localhost:3000/          # preview entry point
docker compose -f docker-compose.base44.yml logs -f web
```

- Host port **3000** → container port **5000** (the preview must be served on 3000).
- The `web` service uses a plain `python:3.12-slim` image with the repo bind-mounted
  and `flask --app app run --debug` (live reload), so edits show up without a rebuild.
- `db` is the Postgres 16 service the app expects. Chain data is **not** stored in it.

## Non-obvious findings

- `app.py` reads `os.environ['DATABASE_URL']` at **import time**, so the app cannot boot
  without it, even though no models/queries exist. The URL comes from compose `environment:`
  (local infra credentials we generate, not a user secret).
- The driver must be pinned: use `postgresql+psycopg2://…`. `requirements.txt` ships
  `psycopg2-binary`, while a bare `postgresql://` URL makes SQLAlchemy 2.x import
  `psycopg` (v3), which is not installed → `ModuleNotFoundError: No module named 'psycopg'`.
- Do not use the repo's own `Dockerfile` for development: `python:3.9-slim-buster` is EOL
  and its `CMD` runs gunicorn with no reload.
- The blockchain lives only in process memory (`Blockchain()` at module import), so any
  reload/restart resets it to the genesis block. Nothing to migrate or seed.
- No external service credentials are needed for this app.

## Verify

```bash
curl -s -X POST http://localhost:3000/mine_block   # -> {"message": "A block is MINED", ...}
curl -s http://localhost:3000/get_chain            # -> {"chain": [...], "length": n}
curl -s http://localhost:3000/is_valid             # -> {"message": "The Blockchain is valid."}
```

Pages: `/` (menu), `/display_block` (mines a block on load), `/display_chain` (lists blocks).

Tests (pytest is not in `requirements.txt`, install it ad hoc inside the container):

```bash
docker compose -f docker-compose.base44.yml exec -T web sh -c "pip install -q pytest && python -m pytest -q"
```
