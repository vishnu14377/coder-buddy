#!/bin/bash

# 🚀 Coder Buddy - Local Mac Runner
# This script starts both backend and frontend servers

echo "🛠️  Starting Coder Buddy Dashboard"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "web_server.py" ]; then
    echo "❌ Please run this script from the coder-buddy root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup_mac.sh first"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with your Groq API key"
    exit 1
fi

print_info "Activating virtual environment..."
source .venv/bin/activate

print_info "Checking if ports are available..."

# Check port 8000
if lsof -i:8000 &> /dev/null; then
    print_warning "Port 8000 is in use. Attempting to free it..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Check port 3000
if lsof -i:3000 &> /dev/null; then
    print_warning "Port 3000 is in use. Attempting to free it..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

print_success "Starting backend server on http://localhost:8000..."

# Start backend in background
python -m uvicorn web_server:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Check if backend started successfully
if curl -s http://localhost:8000/api/health &> /dev/null; then
    print_success "Backend server is running!"
else
    echo "❌ Backend server failed to start. Check the error messages above."
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

print_success "Starting frontend server on http://localhost:3000..."

# Start frontend
cd frontend
yarn start &
FRONTEND_PID=$!

# Give user instructions
echo ""
echo "🎉 Coder Buddy Dashboard is starting!"
echo "=================================="
echo "📡 Backend API: http://localhost:8000"
echo "🎨 Frontend Dashboard: http://localhost:3000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "ℹ️  The frontend will automatically open in your browser"
echo "⏳ Please wait 30-60 seconds for the React app to compile"
echo ""
echo "🛑 To stop the servers, press Ctrl+C"

# Function to cleanup on exit
cleanup() {
    echo ""
    print_info "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    
    # Kill any remaining processes on the ports
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    
    print_success "Servers stopped. Goodbye! 👋"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for user to interrupt
wait