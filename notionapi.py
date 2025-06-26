#!/usr/bin/env python3
"""
JobBuilder - Quick start script
Run this to start the JobBuilder application
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ Error: Please run this script from the JobBuilder directory")
        print("   Current directory:", os.getcwd())
        sys.exit(1)
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("🔧 Virtual environment not found. Please run setup first:")
        print("   ./setup.sh")
        sys.exit(1)
    
    print("🚀 Starting JobBuilder...")
    print("📚 API documentation will be available at: http://localhost:8000/docs")
    print("🌐 Health check available at: http://localhost:8000/")
    print("")
    
    # Start the application
    os.system("source venv/bin/activate && uvicorn app.main:app --reload --port 8000")