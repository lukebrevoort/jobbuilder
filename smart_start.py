#!/usr/bin/env python3
"""
Smart startup script for JobBuilder that handles Railway's PORT properly
"""
import os
import sys
import subprocess

def get_port():
    """Get the port to use, with Railway compatibility"""
    
    # Check various environment variables Railway might use
    port_candidates = [
        os.environ.get('PORT'),
        os.environ.get('SERVER_PORT'), 
        os.environ.get('HTTP_PORT'),
        os.environ.get('APP_PORT')
    ]
    
    print("🔍 Environment debug:")
    print(f"PORT: '{os.environ.get('PORT', 'NOT_SET')}'")
    print(f"SERVER_PORT: '{os.environ.get('SERVER_PORT', 'NOT_SET')}'")
    print(f"All env vars containing 'port':")
    
    for key, value in os.environ.items():
        if 'port' in key.lower():
            print(f"  {key}={value}")
    
    # Find the first valid port
    for port in port_candidates:
        if port and port != '$PORT' and port.isdigit():
            port_num = int(port)
            if 1 <= port_num <= 65535:
                print(f"🎯 Using port: {port_num}")
                return port_num
    
    # Default to 8000
    print("🔧 No valid PORT found, using default: 8000")
    return 8000

def main():
    port = get_port()
    
    print(f"🚀 Starting JobBuilder on port {port}...")
    
    # Start uvicorn
    cmd = [
        "uvicorn", 
        "app.main:app", 
        "--host", "0.0.0.0", 
        "--port", str(port)
    ]
    
    print(f"📋 Running command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
