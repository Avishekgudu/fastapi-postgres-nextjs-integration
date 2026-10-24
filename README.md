# Reference app — the integration checkpoint (answer key)

The finished Part 4 stack: **FastAPI + PostgreSQL + Next.js**, orchestrated with
**Docker Compose**. This is the answer key for the checkpoint — run it if a learner
falls behind, or compare it with your own build.

## Run (one command)

Docker Desktop must be running first.

```bash
cd practice-solutions/reference-app
docker compose up --build
```

Then open:

- Web app — http://localhost:3000 (list items, add a new one)
- API docs — http://localhost:8000/docs
- API JSON — http://localhost:8000/items

Stop with Ctrl+C. To wipe the database too: `docker compose down -v`.

## What you should see

- The page lists two seeded items (Notebook, Pen).
- Adding an item posts to the API, which writes to Postgres; the list refreshes.
- Refreshing the page shows the new item — it persisted in the database.

## How it fits together

| Service | Image / build | Port | Role |
|---------|---------------|------|------|
| `db`  | `postgres:16` | 5432 | Stores the `items` table (seeded by `db/init.sql`) |
| `api` | `./api` (FastAPI) | 8000 | Reads/writes the DB, exposes JSON, enables CORS |
| `web` | `./web` (Next.js) | 3000 | Browser UI that calls the API |

- Services find each other by name on the Compose network (`db`, `api`, `web`).
- `api` waits for `db` via `depends_on: condition: service_healthy` + a healthcheck.
- The browser calls the API at `http://localhost:8000`; CORS allows `http://localhost:3000`.

## Common issues

| Symptom | Fix |
|---------|-----|
| API can't reach DB | Use the service name `db`, not `localhost`; wait for the healthcheck. |
| CORS error in the browser | Confirm `CORS_ORIGINS` includes `http://localhost:3000`. |
| Port already in use | Stop whatever uses 5432 / 8000 / 3000, or change the published port. |

## Push to Git (checkpoint criterion)

```bash
git init
git add .
git commit -m "Integration checkpoint: FastAPI + Postgres + Next.js"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```
