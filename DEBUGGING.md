# Testing 
I testing the end point through PostMan and get to know the problem and debugged it and also perfrom several testing.
# Issue 1

## Symptom

The first dependency install attempt was rejected as an externally managed Python environment.

## Diagnosis

The host Python follows PEP 668 and disallows global package installation.

## Root cause

Using `python3 -m pip install` against the system interpreter.

## Fix

Created a repository-local `backend/.venv` before installing the backend requirements.

## Verification

The virtual environment installed Django and the project dependencies successfully.

# Issue 2

## Symptom

`makemigrations` failed while importing Google verification support.

## Diagnosis

`google.auth.transport.requests` imports the independent `requests` package.

## Root cause

`google-auth` does not install the requests transport dependency by default.

## Fix

Added `requests` explicitly to `backend/requirements.txt`.

## Verification

The migration command completed after this dependency change.

# Issue 3

## Symptom

Host-side Django tests could not connect to PostgreSQL on `localhost:5432`.

## Diagnosis

The project deliberately uses PostgreSQL rather than SQLite and no host database was running.

## Root cause

The expected database is the Compose `postgres` service.

## Fix

Run tests through Docker Compose after the services have started.

## Verification

Compose-based test output is the authoritative verification environment.

# Issue 4

## Symptom

`docker compose up --build` could not pull PostgreSQL.

## Diagnosis

Docker reported it could not connect to the local Docker socket.

## Root cause

The Docker daemon was not running on the development machine.

## Fix

No repository change is required; start Docker Desktop (or the local daemon), then run `docker compose up --build`.

## Verification

`docker compose config` validates the composed service definitions without a daemon.

# Issue 5

## Symptom

Google login appeared to fail with a request error.

## Diagnosis

Nginx returned 502 because the Django backend was unavailable.

## Root cause

The existing PostgreSQL volume contained credentials inconsistent with the current `.env`, so Django could not authenticate to PostgreSQL.

## Fix

The development PostgreSQL database credentials were corrected.

## Verification

Django checks, migrations, and tests passed after the correction.
