# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Visitor Sign-In Log** is a Django REST API for managing visitor sign-in records across multiple buildings, with a planned Phase 4 migration pipeline to ServiceNow.

Stack: Python 3.13, Django 6.0, Django REST Framework, SQLite (dev).

## Commands

```bash
# Activate virtual environment (Windows)
.venv\Scripts\Activate.ps1

# Install dependencies
pip install django djangorestframework

# Apply migrations
python manage.py migrate

# Start dev server (http://127.0.0.1:8000)
python manage.py runserver

# Create new migrations after model changes
python manage.py makemigrations

# Run tests
python manage.py test visitors

# Django shell
python manage.py shell
```

## Architecture

Two Django apps in this repo: `signin_project` (project config) and `visitors` (the sole app with all business logic).

### Models (`visitors/models.py`)

**Building** — `name`, `address` (optional), `building_code` (unique), `phone`

**Visitor** — `first_name`, `last_name`, `email`, `phone`, `building` (FK → Building, CASCADE), `visit_date` (auto), `check_in` (auto), `check_out` (nullable, set on departure)

Deleting a Building cascades to all its Visitors.

### API

DRF's `DefaultRouter` wires two `ModelViewSet`s under `/api/`:

- `/api/buildings/` — full CRUD for buildings
- `/api/visitors/` — full CRUD for visitors

The browsable API is available at `http://127.0.0.1:8000/api/`.

### URL routing

`signin_project/urls.py` mounts `visitors/urls.py` at `/api/`. The `visitors/urls.py` uses `DefaultRouter` to register both viewsets.

### Migrations

- `0001_initial.py` — creates Building and Visitor
- `0002_visitor_check_in_visitor_check_out.py` — adds check_in/check_out to Visitor

To reset the dev database: delete `db.sqlite3` and re-run `python manage.py migrate`.

## Scripts

`scripts/api_client.py` — standalone REST client demo. Exercises full CRUD against the live API. Run with `python scripts/api_client.py` while the dev server is up. Mirrors ServiceNow REST Message patterns (endpoint URL, HTTP method, JSON payload).

## Management Commands

```bash
# Seed the database with sample buildings and visitors (clears existing data first)
python manage.py seed_data
```

`visitors/management/commands/seed_data.py` — creates 5 buildings and 12 visitors; sets `check_out` on every third visitor to simulate a mix of active and departed visitors.

## Tests

`visitors/tests.py` uses DRF's `APIClient` (not `requests`). Two test classes:

- `BuildingAPITests` — list, create, duplicate `building_code` rejection, delete
- `VisitorAPITests` — list, create, invalid building FK rejection, PATCH checkout, cascade delete on building delete

## Roadmap

- [x] Phase 1 — Django REST API with Building and Visitor models
- [x] Phase 2 — REST client (`scripts/api_client.py`) and API test suite
- [ ] Phase 3 — ServiceNow developer instance setup
- [ ] Phase 4 — Python migration script (API → ServiceNow)
