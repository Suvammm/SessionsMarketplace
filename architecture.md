## Architecture

The application follows a simple full-stack architecture:

```text
                    ┌──────────────────────┐
                    │       Browser        │
                    │   React / Vite UI    │
                    └──────────┬───────────┘
                               │
                               │ HTTP
                               ▼
                    ┌──────────────────────┐
                    │        Nginx         │
                    │   Reverse Proxy      │
                    │      Port 8080       │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    │                      │
                    ▼                      ▼
          ┌──────────────────┐   ┌──────────────────┐
          │ React Frontend   │   │ Django REST API  │
          │                  │   │                  │
          │ Sessions UI      │   │ Authentication   │
          │ Bookings UI      │   │ Sessions         │
          │ Profile          │   │ Bookings         │
          │ Creator UI       │   │ Authorization    │
          └──────────────────┘   └────────┬─────────┘
                                          │
                                          │ SQL
                                          ▼
                                 ┌──────────────────┐
                                 │   PostgreSQL     │
                                 │                  │
                                 │ Users            │
                                 │ Sessions         │
                                 │ Bookings         │
                                 └──────────────────┘
                                          │
                                          │ Docker Volume
                                          ▼
                                 ┌──────────────────┐
                                 │  postgres_data   │
                                 │ Persistent Data  │
                                 └──────────────────┘
