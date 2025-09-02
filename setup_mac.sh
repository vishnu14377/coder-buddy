#!/bin/bash

# 🍎 Coder Buddy - Mac Setup Script
# This script will help you set up the application on your local Mac

echo "🛠️  Coder Buddy - Mac Setup Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS. Please follow manual setup instructions."
    exit 1
fi

print_status "Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.11+ using: brew install python@3.11"
    exit 1
fi

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js found: $NODE_VERSION"
else
    print_error "Node.js not found. Please install using: brew install node"
    exit 1
fi

# Check Yarn
if command -v yarn &> /dev/null; then
    YARN_VERSION=$(yarn --version)
    print_success "Yarn found: $YARN_VERSION"
else
    print_error "Yarn not found. Please install using: brew install yarn"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "web_server.py" ]; then
    print_error "Please run this script from the coder-buddy root directory (where web_server.py is located)"
    exit 1
fi

print_status "Setting up Python virtual environment..."

# Create virtual environment
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
source .venv/bin/activate
print_success "Virtual environment activated"

print_status "Installing Python dependencies..."

# Install Python dependencies
pip install --upgrade pip
pip install groq langchain langchain-core langchain-groq langgraph pydantic python-dotenv fastapi uvicorn websockets

print_success "Python dependencies installed"

print_status "Setting up frontend..."

# Check if frontend directory exists
if [ -d "frontend" ]; then
    cd frontend
    print_status "Installing frontend dependencies..."
    yarn install
    print_success "Frontend dependencies installed"
    cd ..
else
    print_error "Frontend directory not found. Please ensure all project files are present."
    exit 1
fi

print_status "Setting up environment file..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "GROQ_API_KEY=your_groq_api_key_here" > .env
    print_warning "Created .env file. Please add your Groq API key from https://console.groq.com/keys"
    print_warning "Edit .env file and replace 'your_groq_api_key_here' with your actual API key"
else
    print_warning ".env file already exists. Make sure it contains your Groq API key"
fi

print_success "Setup completed successfully!"

echo ""
echo "🚀 To start the application:"
echo "=================================="
echo "1. Make sure you've added your Groq API key to .env file"
echo "2. Open two terminals in VSCode or your terminal app"
echo ""
echo "Terminal 1 (Backend):"
echo "  source .venv/bin/activate"
echo "  python -m uvicorn web_server:app --host 127.0.0.1 --port 8000 --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  yarn start"
echo ""
echo "Then open http://localhost:3000 in your browser"
echo ""
echo "🔧 Or use the automated startup script:"
echo "  source .venv/bin/activate && python start_dashboard.py"

echo ""
print_success "Happy coding! 🎉"