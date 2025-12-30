# Mind Matrix — Storytelling API

> **Powering immersive journals, blogs, series, and events** with a modern Django REST backend.

Welcome to the Django + DRF server that fuels the Mind Matrix storytelling platform. This README helps you understand the architecture, configure your environment, and run the project locally or in production.

---

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Tech Stack](#tech-stack)
4. [Service Architecture](#service-architecture)
5. [API Surface](#api-surface)
6. [Environment Setup](#environment-setup)
7. [Running Locally](#running-locally)
8. [Project Structure](#project-structure)
9. [Operations & Tooling](#operations--tooling)
10. [Security Notes](#security-notes)
11. [Roadmap Ideas](#roadmap-ideas)
12. [License](#license)

---

## Overview
Mind Matrix exposes a rich storytelling API that powers journals, blogs, episodic series, and community events. The service is built on **Django 5** with **Django REST Framework**, offering JWT-based authentication, flexible filtering, and polished email onboarding workflows.@server/aurora_backend/settings.py#21-188 @server/accounts/views.py#17-108 @server/newsletter/views.py#14-170

- **Audience**: client/mobile apps, integrations, internal tooling.
- **Goal**: deliver a secure, scalable API with intuitive endpoints for creative storytelling experiences.
- **Status**: MVP-ready with pluggable auth, content management, and newsletter engagement.

---

## Key Features
- 🔐 **JWT Authentication & Custom User Model** with extended profile fields, social links, and follower stats.@server/accounts/models.py#1-62 @server/accounts/urls.py#11-18
- 📰 **Content Engine** covering categories, posts, series, seasons, comments, likes, and events — all filterable and slug-driven.@server/blog/models.py#9-248 @server/blog/views.py#23-191
- 📨 **Newsletter Funnel** that activates a 24-day trial and dispatches branded welcome emails via templated HTML.@server/newsletter/views.py#14-170
- ⚙️ **Configurable Settings** for PostgreSQL (local & Neon), CORS origins, JWT lifetimes, and email providers via `.env` variables.@server/aurora_backend/settings.py#73-188 @server/.env.example#1-27
- 🛡️ **Granular Permissions** through DRF plus custom `IsAuthorOrReadOnly` safeguards for write operations.@server/blog/views.py#32-178

---

## Tech Stack

| Layer            | Choice                                      | Notes |
|------------------|---------------------------------------------|-------|
| Framework        | Django 5.0.1                                | Modern async-capable backend |
| API Toolkit      | Django REST Framework 3.14                  | Serializers, viewsets, pagination |
| Auth             | djangorestframework-simplejwt 5.3           | Access/refresh JWT tokens |
| Database         | PostgreSQL (psycopg2)                       | Local or Neon cloud via `DATABASE_URL` |
| Config           | python-decouple, dj-database-url            | `.env` driven configuration |
| Email            | Django email backends (SMTP / SendGrid etc.)| HTML onboarding campaign |

Dependencies are pinned in [`requirements.txt`](./requirements.txt).

---

## Service Architecture
- **Core Settings** live in `aurora_backend/settings.py`, enabling modular apps, CORS, JWT tuning, and environment-driven configuration.@server/aurora_backend/settings.py#21-188
- **Accounts App** implements a custom `User` model, registration, profile edits, and follow/unfollow flows.@server/accounts/models.py#1-62 @server/accounts/views.py#17-108
- **Blog App** orchestrates storytelling entities (categories, posts, series, seasons, comments, likes, events) with slug-based routing and analytics counters.@server/blog/models.py#9-248 @server/blog/views.py#80-178
- **Newsletter App** captures subscribers, applies trial periods, and sends rich HTML emails using the configured provider.@server/newsletter/views.py#14-170
- **Routing** consolidates under `/api/...` namespaces via `aurora_backend/urls.py`.@server/aurora_backend/urls.py#9-19

---

## API Surface
| Namespace         | Description |
|-------------------|-------------|
| `/api/auth/`      | Registration, login (JWT), refresh, profile CRUD, follow/unfollow. @server/accounts/urls.py#11-18 |
| `/api/blog/`      | CRUD for categories, series, seasons, posts, events, comments, likes, featured/upcoming helpers. @server/blog/views.py#23-191 |
| `/api/newsletter/`| Newsletter subscription endpoint triggering welcome email + trial. @server/newsletter/urls.py#1-6 |

Pagination defaults to page size 10 with search and ordering filters available on most list endpoints.@server/aurora_backend/settings.py#137-151 @server/blog/views.py#32-188

---

## Environment Setup
1. Copy `.env.example` to `.env` and adjust secrets, database settings, and email backend.@server/.env.example#1-27
2. Set `DATABASE_URL` (for Neon/Prod) **or** individual `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` fields for local development.@server/aurora_backend/settings.py#73-99
3. Configure `CORS_ALLOWED_ORIGINS` and `FRONTEND_URL` to match your deployed client.@server/aurora_backend/settings.py#165-188
4. Make sure `SECRET_KEY` and JWT lifetimes suit your environment.@server/aurora_backend/settings.py#13-163

---

## Running Locally
### Prerequisites
- **Python** ≥ 3.11 (virtual environment recommended)
- **PostgreSQL** 14+ (or Neon connection string)

### Quick Start
```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create a superuser (optional but recommended)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

---

## Project Structure
```text
server/
├─ aurora_backend/        # Core project settings & URLs
├─ accounts/              # Custom user model, auth endpoints
├─ blog/                  # Storytelling domain (posts, series, events)
├─ newsletter/            # Subscriber capture & welcome campaign
├─ manage.py
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## Operations & Tooling
- **Admin Panel**: `http://localhost:8000/admin/` with your superuser credentials.
- **Static & Media**: served from `STATIC_ROOT`/`MEDIA_ROOT` locally; configure cloud storage for production.@server/aurora_backend/settings.py#122-188
- **Testing**: `python manage.py test` runs Django/DRF test suites.
- **Linting**: Add `flake8`/`black` to enforce style (not yet configured).

---

## Security Notes
- Rotate `SECRET_KEY` and JWT signing keys before deploying to production.@server/aurora_backend/settings.py#13-163
- Enforce HTTPS and add production domains to `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`.
- Swap the console email backend for a transactional provider in production.@server/.env.example#1-27
- Monitor follower/like counters for abuse; consider throttling endpoints via DRF settings.

---

## Roadmap Ideas
1. Implement rate limiting with `REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES']`.
2. Add search indexing (e.g., Elasticsearch) for posts and events.
3. Extend newsletter flows with webhooks and unsubscribe endpoints.
4. Introduce S3-compatible storage for media assets.

---

## License
This backend is proprietary to the Mind Matrix team. Contact the maintainers for licensing or partnership inquiries.
