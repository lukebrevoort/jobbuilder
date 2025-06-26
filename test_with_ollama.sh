#!/bin/bash

# Local Ollama Test Script
echo "🧪 Testing JobBuilder with Local Ollama..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📦 Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
fi

# Check if model is available
echo "🤖 Checking AI model..."
if ! ollama list | grep -q "llama3.2:1b"; then
    echo "⬇️  Downloading AI model (this may take a few minutes)..."
    ollama pull llama3.2:1b
fi

# Start Ollama in background
echo "🚀 Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Test Ollama
echo "🧪 Testing Ollama..."
ollama run llama3.2:1b "Hello, just respond with 'Working!'" --verbose

# Start JobBuilder
echo "🚀 Starting JobBuilder..."
source venv/bin/activate
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama3.2:1b
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
JOBBUILDER_PID=$!

echo ""
echo "🎉 Both services are running!"
echo "📚 JobBuilder API: http://localhost:8000/docs"
echo "🤖 Ollama API: http://localhost:11434"
echo ""
echo "Press any key to stop both services..."
read -n 1

# Clean up
kill $OLLAMA_PID 2>/dev/null
kill $JOBBUILDER_PID 2>/dev/null
echo "✅ Services stopped."
