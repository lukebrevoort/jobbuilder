#!/bin/bash
set -e

# Debug environment variables
echo "🔍 Environment debug:"
echo "PORT env var: '${PORT}'"
echo "All PORT-related vars:"
env | grep -i port || echo "No PORT vars found"

# Determine port to use
if [ -z "$PORT" ] || [ "$PORT" = "\$PORT" ] || [ "$PORT" = "" ]; then
    echo "🔧 PORT not set or invalid, using default 8000"
    ACTUAL_PORT=8000
else
    echo "🎯 Using PORT from environment: $PORT"
    ACTUAL_PORT=$PORT
fi

echo "🚀 Starting JobBuilder on port $ACTUAL_PORT..."

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port $ACTUAL_PORT
