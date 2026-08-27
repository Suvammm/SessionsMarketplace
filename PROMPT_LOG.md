## Prompt 1: Initial Sessions Marketplace Implementation

**Tool/Model:** Codex

**Prompt/Task:**  
Build the Sessions Marketplace assignment using React/Vite for the frontend, Django REST Framework for the backend, PostgreSQL for the database, Google OAuth with JWT authentication, Docker Compose, and Nginx. Implement User and Creator roles, session management, bookings, backend authorization, and concurrency-safe booking capacity.

**What I Used:**  
Used the generated project structure and implementation as the starting point for the application, including the frontend, Django backend, PostgreSQL configuration, Docker Compose setup, authentication flow, sessions, bookings, and role-based functionality.

**What I Changed/Rejected:**  
Reviewed and corrected implementation issues encountered during development rather than accepting the generated implementation blindly. In particular, capacity enforcement was kept on the backend using PostgreSQL transactions/locking rather than relying on frontend seat checks.

**How I Verified It:**  
Verified the Docker Compose configuration, Django checks, migrations, backend tests, frontend build, authentication flow, session creation, booking flow, and concurrency test.