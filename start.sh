#!/bin/bash
set -e

# Use PORT environment variable if set, otherwise default to 8000
PORT=${PORT:-8000}

echo "Starting JobBuilder on port $PORT..."

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
