# Sessions Marketplace

## Overview

A compact marketplace where people browse and book sessions while creators manage their own catalog.

## Features

- Google ID-token sign-in exchanged for Django JWT access and refresh tokens.
- Public catalog, details, profile, bookings, and creator dashboard.
- Backend-enforced creator roles and ownership checks.
- Capacity-safe active bookings backed by PostgreSQL row locking.

## Tech Stack & Architecture

React/Vite → Nginx → Django REST Framework → PostgreSQL. Nginx is the only browser-facing service; it routes `/api/` to Django and everything else to the built React app.

## Project Structure

`backend/` contains Django applications; `frontend/` contains React; `nginx/` contains the proxy configuration.

## Prerequisites

Docker Compose and a Google OAuth Web client. Copy `.env.example` to `.env`, set a strong `DJANGO_SECRET_KEY`, and enter PostgreSQL and Google credentials. In Google Cloud, add the deployed origin (for local Compose: `http://localhost:8080`) to Authorized JavaScript origins.

Required environment variables are `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `GOOGLE_CLIENT_ID`, `JWT_ACCESS_LIFETIME`, and `JWT_REFRESH_LIFETIME`.

## Running the Application

```sh
cp .env.example .env
docker compose up --build
```

Open http://localhost:8080. New users choose User or Creator once after Google sign-in; the backend persists that choice and continues to enforce it for creator endpoints.

## Running Tests

```sh
docker compose run --rm backend python manage.py test
```

To run the concurrency test alone:

```sh
docker compose run --rm backend python manage.py test bookings.tests.BookingConcurrencyTests
```

Tests run against the PostgreSQL service. The included tests cover invalid JWTs, creator authorization, duplicate bookings, started sessions, and a two-thread capacity-one race.

## Demo Accounts

These accounts are provided only for assignment evaluation.

- Demo User — username: `demo_user`; password: `demo_user_password`
- Demo Creator — username: `demo_creator`; password: `demo_creator_password`

Create or reset the public demo accounts after Docker starts:

```sh
docker compose exec backend python manage.py create_demo_users
```

## API Overview

- `POST /api/auth/google/`, `GET /api/auth/me/`, `PATCH /api/auth/profile/`, `POST /api/auth/token/refresh/`
- `GET|POST /api/sessions/`, `GET|PATCH|DELETE /api/sessions/:id/`
- `POST /api/sessions/:id/book/`, `GET /api/bookings/`, `GET /api/creator/sessions/`

## Authentication Flow

Google returns an ID token to React. React sends it to Django, which verifies it with Google and returns JWT access/refresh tokens. The API service attaches the access token and refreshes once after a 401.

## Booking Concurrency

Booking locks the session row using `transaction.atomic()` and `select_for_update()`. Started, duplicate, and capacity conditions are checked and the booking is created in that same transaction. PostgreSQL's conditional unique constraint also prevents two ACTIVE bookings by one user for one session.

## Database Persistence

The named `postgres_data` volume preserves database files when frontend/backend containers are restarted.

## Known Limitations

Role selection is intentionally one-time and requires no approval workflow. Cancellations are API-model-ready but not exposed in the UI. Token storage uses localStorage, appropriate only for this assessment.

## What I Would Improve With Another Day

Add cancellation, pagination/filtering, httpOnly-cookie auth, production CORS/HTTPS settings, and a dedicated PostgreSQL concurrency integration test in CI.
# SessionsMarketplace
