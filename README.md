# Visitor Sign-In Log

A Django REST API for managing visitor sign-in records across multiple buildings, with a Python migration pipeline to ServiceNow.

## Overview

This project provides a complete visitor management system built as a Django REST API. It tracks visitor check-ins, host information, badge assignments, and building locations. A Python migration script bridges the data from the API to ServiceNow for enterprise integration.

## Tech Stack

- **Python 3.13**
- **Django 6.0** — Web framework
- **Django REST Framework** — RESTful API layer
- **SQLite** — Development database
- **ServiceNow** — Target migration platform (Phase 2)

## Project Structure

```
visitor-signin-log/
├── signin_project/        # Django project settings and configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── visitors/              # Main application
│   ├── models.py          # Building and Visitor data models
│   ├── serializers.py     # JSON serialization
│   ├── views.py           # API viewsets
│   └── urls.py            # API route definitions
├── db.sqlite3             # SQLite database (dev only)
└── manage.py
```

## Data Models

### Building

| Field         | Type      | Description              |
|---------------|-----------|--------------------------|
| id            | Auto      | Primary key              |
| name          | CharField | Building name            |
| address       | CharField | Building address         |
| building_code | CharField | Unique building code     |
| phone         | CharField | building phone           |

### Visitor


first_name": "Alex",
        "last_name": "Naranjo",
        "email": "alex.naranjo.m@gmail.com",
        "phone": "3012223327",
        "visit_date": "2026-05-08T05:05:46.121754Z",
        "check_in": "2026-05-08T05:05:46.121839Z",
        "check_out": "2026-05-01T15:06:00Z",

| Field           | Type          | Description                  |
|-----------------|---------------|------------------------------|
| id              | Auto          | Primary key                  |
| first_name      | CharField     | Visitor's first name         |
| last_name       | CharField     | Visitor's last name          |
| visitor_email   | EmailField    | Visitor's email              |
| visitor_phone   | CharField     | Visitor's phone              |
| building        | ForeignKey    | Building visited (FK)        |
| check_in        | DateTimeField | Auto-set on creation         |
| check_out       | DateTimeField | Nullable, set on departure   |

## API Endpoints

| Method | Endpoint              | Description          |
|--------|-----------------------|----------------------|
| GET    | `/api/buildings/`     | List all buildings   |
| POST   | `/api/buildings/`     | Create a building    |
| GET    | `/api/buildings/:id/` | Get a building       |
| PUT    | `/api/buildings/:id/` | Update a building    |
| DELETE | `/api/buildings/:id/` | Delete a building    |
| GET    | `/api/visitors/`      | List all visitors    |
| POST   | `/api/visitors/`      | Create a visitor     |
| GET    | `/api/visitors/:id/`  | Get a visitor        |
| PUT    | `/api/visitors/:id/`  | Update a visitor     |
| DELETE | `/api/visitors/:id/`  | Delete a visitor     |

## Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/visitor-signin-log.git
cd visitor-signin-log

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install django djangorestframework

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/api/` to access the browsable API.

## Roadmap

- [x] Phase 1 — Django REST API with Building and Visitor models
- [ ] Phase 2 — Sample data population
- [ ] Phase 3 — ServiceNow developer instance setup
- [ ] Phase 4 — Python migration script (API → ServiceNow)

## License

MIT
