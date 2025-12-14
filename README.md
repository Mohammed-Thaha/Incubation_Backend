# Incubation_Backend

A Python backend project (event calendar service) providing an API for managing events. The repository contains a small Python package `event_calendar` that implements database models, schemas, CRUD operations and an application entrypoint — likely implemented with a modern web framework such as FastAPI.

This README provides an overview of the repository, how to run the project locally and with Docker, useful references to files in the repo, and guidance for contributing.

---

## Repository snapshot

Top-level files
- [.dockerignore](https://github.com/Mohammed-Thaha/Incubation_Backend/blob/main/.dockerignore)
- [Dockerfile](https://github.com/Mohammed-Thaha/Incubation_Backend/blob/main/Dockerfile)
- [docker-compose.yml](https://github.com/Mohammed-Thaha/Incubation_Backend/blob/main/docker-compose.yml)
- [requirements.txt](https://github.com/Mohammed-Thaha/Incubation_Backend/blob/main/requirements.txt)

Package: `event_calendar/`
- `event_calendar/.gitignore`
- `event_calendar/__init__.py`
- `event_calendar/crud.py`       — database CRUD operations
- `event_calendar/database.py`   — database session / engine setup
- `event_calendar/main.py`       — application entrypoint (API routes)
- `event_calendar/models.py`     — ORM models
- `event_calendar/schemas.py`    — request/response schemas (Pydantic)

This structure indicates a typical API service layout (models, schemas, CRUD, and an app startup file).

---

## Quickstart

These instructions assume you have Python 3.9+ installed and access to Docker if you prefer containerized execution.

### 1) Install dependencies (local)
1. Create a virtual environment
   - python -m venv .venv
   - source .venv/bin/activate  (Windows: .venv\Scripts\activate)
2. Install requirements
   - pip install -r requirements.txt

Note: the repository includes a `requirements.txt` file at the project root.

### 2) Run the application (typical local approach)
With the dependencies installed, start the app. The repository's entrypoint is `event_calendar/main.py`. A common command (if using FastAPI + Uvicorn) would be:
- uvicorn event_calendar.main:app --reload

If the code uses a different server, refer to `event_calendar/main.py` for exact startup instructions and exported app callable.

### 3) Run with Docker
Build and run the containerized service:
- docker build -t incubation-backend .
- docker run --env-file .env -p 8000:8000 incubation-backend

Or use docker-compose (the repo includes `docker-compose.yml`):
- docker-compose up --build

The included `Dockerfile` and `docker-compose.yml` provide the container configuration. Check them for environment variable names (database URLs, ports, etc.).

---

## Configuration

The application most likely expects environment variables for database configuration. Check `event_calendar/database.py` and `docker-compose.yml` to see the exact variable names (commonly `DATABASE_URL` or `SQLALCHEMY_DATABASE_URL`). Provide a `.env` file or pass env vars via Docker.

Example (common pattern):
- DATABASE_URL=postgresql://user:password@db:5432/incubation
- APP_PORT=8000

---

## API (overview)

The repository contains `event_calendar/main.py`, `schemas.py`, and `crud.py`, which suggests the following typical endpoints are implemented (confirm exact route names in `main.py`):

- GET /events            — list all events
- GET /events/{id}       — get a single event by id
- POST /events           — create a new event
- PUT /events/{id}       — update an event
- DELETE /events/{id}    — delete an event

Example request to create an event (JSON):
{
  "title": "Demo Event",
  "start_time": "2025-01-01T10:00:00Z",
  "end_time": "2025-01-01T11:00:00Z",
  "description": "Short description"
}

Example curl (adjust host/port and payload to match your implementation):
- curl -X GET http://localhost:8000/events
- curl -X POST http://localhost:8000/events -H "Content-Type: application/json" -d '{"title":"Demo","start_time":"2025-01-01T10:00:00Z","end_time":"2025-01-01T11:00:00Z"}'

Open the app root or `/docs` (if FastAPI + Swagger is used) in your browser for interactive API docs.

---

## License

No license file detected in the repository snapshot. Add a LICENSE file to make usage terms explicit (for example, MIT License).

---
