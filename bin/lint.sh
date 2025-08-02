#!/bin/bash

# Linting and formatting script for Docker
# Usage: bin/lint.sh [options]
# Options:
#   --fix, -f     Fix issues automatically (format code and apply safe fixes)
#   --check, -c   Check only (default)
#   --mypy        Run type checking with mypy
#   --all         Run all checks (ruff + mypy)
#   --help, -h    Show this help message

set -e

# Default options
RUN_RUFF=true
RUN_MYPY=false
FIX_MODE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --fix|-f)
            FIX_MODE=true
            shift
            ;;
        --check|-c)
            FIX_MODE=false
            shift
            ;;
        --mypy)
            RUN_MYPY=true
            shift
            ;;
        --all)
            RUN_MYPY=true
            shift
            ;;
        --help|-h)
            echo "Linting and formatting script for Docker"
            echo ""
            echo "Usage: bin/lint.sh [options]"
            echo ""
            echo "Options:"
            echo "  --fix, -f     Fix issues automatically (format code and apply safe fixes)"
            echo "  --check, -c   Check only (default)"
            echo "  --mypy        Run type checking with mypy"
            echo "  --all         Run all checks (ruff + mypy)"
            echo "  --help, -h    Show this help message"
            echo ""
            echo "Examples:"
            echo "  bin/lint.sh              # Check code with ruff"
            echo "  bin/lint.sh --fix        # Format code and fix issues"
            echo "  bin/lint.sh --mypy       # Run type checking"
            echo "  bin/lint.sh --all        # Run all checks"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

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

echo "🔍 Running code quality checks..."
echo ""

# Run Ruff checks
if [ "$RUN_RUFF" = true ]; then
    if [ "$FIX_MODE" = true ]; then
        echo "🔧 Formatting code with ruff..."
        docker compose -f docker-compose.local.yml exec django ruff format .
        echo ""
        
        echo "🔧 Fixing issues with ruff..."
        docker compose -f docker-compose.local.yml exec django ruff check . --fix
        echo ""
    else
        echo "🔍 Checking code with ruff..."
        docker compose -f docker-compose.local.yml exec django ruff check .
        echo ""
        
        echo "🔍 Checking code formatting with ruff..."
        docker compose -f docker-compose.local.yml exec django ruff format --check .
        echo ""
    fi
fi

# Run mypy type checking
if [ "$RUN_MYPY" = true ]; then
    echo "🔍 Running type checks with mypy..."
    docker compose -f docker-compose.local.yml exec django mypy opswat_backend
    echo ""
fi

if [ "$FIX_MODE" = true ]; then
    echo "✅ Code formatting and fixing completed!"
else
    echo "✅ Code quality checks completed!"
fi