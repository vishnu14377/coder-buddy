#!/usr/bin/env python3
"""
Quick test script to verify local setup is working
"""

import os
import sys
import requests
import subprocess
import time
from pathlib import Path

def test_python_environment():
    """Test Python environment and dependencies"""
    print("🐍 Testing Python Environment...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python version too old: {python_version}")
        return False
    
    # Test key imports
    try:
        import langchain_google_genai
        print("✅ Google Generative AI library imported")
    except ImportError:
        print("❌ Google Generative AI library not found")
        return False
    
    try:
        import langchain
        print("✅ LangChain library imported")
    except ImportError:
        print("❌ LangChain library not found")
        return False
    
    try:
        import fastapi
        print("✅ FastAPI library imported")
    except ImportError:
        print("❌ FastAPI library not found")
        return False
    
    return True

def test_environment_file():
    """Test if .env file exists and has API key"""
    print("\n🔐 Testing Environment Configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    if "GROQ_API_KEY" in content:
        if "your_groq_api_key_here" in content:
            print("⚠️  .env file exists but contains placeholder API key")
            print("   Please replace 'your_groq_api_key_here' with your actual Groq API key")
            return False
        else:
            print("✅ .env file configured with API key")
            return True
    else:
        print("❌ GROQ_API_KEY not found in .env file")
        return False

def test_frontend_setup():
    """Test if frontend is properly set up"""
    print("\n🎨 Testing Frontend Setup...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ package.json not found in frontend directory")
        return False
    
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("❌ node_modules not found. Run 'cd frontend && yarn install'")
        return False
    
    print("✅ Frontend setup looks good")
    return True

def test_backend_import():
    """Test if backend can be imported"""
    print("\n📡 Testing Backend Import...")
    
    try:
        from agent.graph import route_request
        print("✅ Agent system can be imported")
    except ImportError as e:
        print(f"❌ Cannot import agent system: {e}")
        return False
    
    try:
        import web_server
        print("✅ Web server can be imported")
    except ImportError as e:
        print(f"❌ Cannot import web server: {e}")
        return False
    
    return True

def test_project_structure():
    """Test if all required files are present"""
    print("\n📁 Testing Project Structure...")
    
    required_files = [
        "web_server.py",
        "main.py",
        "agent/graph.py",
        "agent/qa_agent.py",
        "frontend/package.json",
        "frontend/src/App.js",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Run all tests"""
    print("🧪 Coder Buddy - Local Setup Test")
    print("=" * 40)
    
    tests = [
        test_project_structure,
        test_python_environment,
        test_environment_file,
        test_frontend_setup,
        test_backend_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup looks good.")
        print("\n🚀 To start the application:")
        print("   ./run_local.sh")
        print("\n🎯 Or manually:")
        print("   Terminal 1: source .venv/bin/activate && python -m uvicorn web_server:app --host 127.0.0.1 --port 8000 --reload")
        print("   Terminal 2: cd frontend && yarn start")
    else:
        print("❌ Some tests failed. Please fix the issues above before running the application.")
        
        if passed < total // 2:
            print("\n💡 Quick fix suggestions:")
            print("   1. Run: ./setup_mac.sh")
            print("   2. Add your Groq API key to .env file")
            print("   3. Run: cd frontend && yarn install")

if __name__ == "__main__":
    main()