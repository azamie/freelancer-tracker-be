#!/bin/bash

# Django management script for Docker
# Usage: bin/manage.sh <command> [args...]
# Examples:
#   bin/manage.sh migrate
#   bin/manage.sh createsuperuser
#   bin/manage.sh shell
#   bin/manage.sh makemigrations
#   bin/manage.sh collectstatic --noinput

set -e

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root directory
cd "$PROJECT_ROOT"

# Check if docker-compose.local.yml exists
if [ ! -f "docker-compose.local.yml" ]; then
    echo "Error: docker-compose.local.yml not found in project root"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Execute Django management command in Docker container
docker compose -f docker-compose.local.yml exec django python manage.py "$@"