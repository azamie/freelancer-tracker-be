# OPSWAT Backend

OPSWAT Entrance Test - Django REST API application

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Developer Setup (Docker)

### Prerequisites

- Docker Desktop installed and running
- Docker Compose v2
- Git

### Quick Start

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd opswat_backend
   ```

2. **Set up environment files**

   ```bash
   # Copy environment example files
   cp .env.example .envs/local/.env
   ```

   Edit the environment files if needed to customize settings.

3. **Build and start the application**

   ```bash
   # Build containers
   docker compose -f docker-compose.local.yml build

   # Start all services
   docker compose -f docker-compose.local.yml up -d

   # View logs (optional)
   docker compose -f docker-compose.local.yml logs -f django
   ```

4. **Run database migrations and collect static files**

   ```bash
   # Run database migrations
   bin/manage.sh migrate

   # Collect static files for admin interface styling
   bin/manage.sh collectstatic --noinput
   ```

5. **Create a superuser account**

   ```bash
   bin/manage.sh createsuperuser
   ```

6. **Access the application**
   - API: http://localhost:8000
   - Admin: http://localhost:8000/admin
