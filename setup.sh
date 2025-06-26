#!/bin/bash

# JobBuilder Quick Setup Script
echo "🚀 Setting up JobBuilder..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file from example
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✏️  Please edit .env file with your Notion API credentials"
fi

# Create output directory
echo "📁 Creating output directory..."
mkdir -p output

# Run basic functionality test
echo "🧪 Running basic functionality test..."
python test_setup.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your Notion API key and database ID"
echo "2. Edit data/personal_info.json with your personal information"
echo "3. Edit data/base_resume.json with your resume data"
echo "4. Start the server: uvicorn app.main:app --reload --port 8000"
echo ""
echo "🌐 Server will be available at: http://localhost:8000"
echo "📚 API docs will be available at: http://localhost:8000/docs"
