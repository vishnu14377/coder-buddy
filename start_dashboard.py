#!/usr/bin/env python3
"""
Startup script for Coder Buddy Dashboard
Runs both FastAPI backend and React frontend
"""

import subprocess
import sys
import time
import os
import threading
from pathlib import Path

def run_backend():
    """Run the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "web_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], cwd="/app")
    except KeyboardInterrupt:
        print("Backend server stopped.")

def run_frontend():
    """Run the React frontend development server"""
    print("🎨 Starting React frontend server...")
    try:
        env = os.environ.copy()
        env['PORT'] = '3000'
        subprocess.run([
            "yarn", "start"
        ], cwd="/app/frontend", env=env)
    except KeyboardInterrupt:
        print("Frontend server stopped.")

def main():
    print("🛠️  Starting Coder Buddy Dashboard")
    print("=" * 50)
    
    # Check if required directories exist
    if not Path("/app/frontend").exists():
        print("❌ Frontend directory not found!")
        return
    
    if not Path("/app/.env").exists():
        print("❌ .env file not found! Please create it with your GROQ_API_KEY")
        return
    
    print("✅ All required files found")
    print("📡 Backend will run on: http://localhost:8000")
    print("🌐 Frontend will run on: http://localhost:3000")
    print("=" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(3)
    
    # Start frontend (this will block)
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Coder Buddy Dashboard...")
        print("Thanks for using Coder Buddy! 👋")

if __name__ == "__main__":
    main()