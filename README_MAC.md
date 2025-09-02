# 🍎 Coder Buddy - Mac Setup & Usage Guide

## 🚀 **Quick Start (TL;DR)**

```bash
# 1. Setup (one-time)
./setup_mac.sh

# 2. Add your Groq API key to .env file
# Get key from: https://console.groq.com/keys

# 3. Run the application
./run_local.sh

# 4. Open http://localhost:3000 in your browser
```

---

## 📋 **Detailed Setup Instructions**

### **Step 1: Download/Clone the Project**

If you have the project files, navigate to the directory in Terminal:
```bash
cd /path/to/coder-buddy
```

### **Step 2: Run the Setup Script**

```bash
# Make the script executable and run it
chmod +x setup_mac.sh
./setup_mac.sh
```

This script will:
- ✅ Check if Python 3, Node.js, and Yarn are installed
- ✅ Create a Python virtual environment
- ✅ Install all Python dependencies
- ✅ Install all frontend dependencies
- ✅ Create a basic .env file

### **Step 3: Get Your Groq API Key**

1. Go to [https://console.groq.com/keys](https://console.groq.com/keys)
2. Create an account and generate an API key
3. Edit the `.env` file and replace `your_groq_api_key_here` with your actual key:

```bash
# Edit .env file
nano .env

# Or use VSCode
code .env
```

### **Step 4: Test Your Setup**

```bash
python test_local_setup.py
```

This will verify everything is configured correctly.

### **Step 5: Start the Application**

```bash
./run_local.sh
```

---

## 🎯 **Using VSCode (Recommended)**

### **Open in VSCode**
```bash
code .
```

### **Recommended Extensions**
VSCode will automatically suggest these extensions (click "Install" when prompted):
- Python
- Pylance  
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Thunder Client (for API testing)

### **VSCode Tasks**
Press `Cmd+Shift+P` and type "Tasks: Run Task" to see these options:
- 🚀 **Start Full Stack** - Runs both backend and frontend
- 🔧 **Setup Mac Environment** - Runs the setup script
- 📦 **Install Dependencies** - Reinstalls Python packages
- 🎨 **Start Frontend Only** - Runs just the React app
- 📡 **Start Backend Only** - Runs just the API server

### **VSCode Debugging**
Press `F5` or go to Run and Debug panel:
- 🚀 **Start Backend Server** - Runs backend with debugging
- 🧪 **Test Q&A Agent** - Tests the AI functionality  
- 🛠️ **Run CLI Mode** - Runs the command-line interface

---

## 🌐 **Application URLs**

Once running, you can access:
- **🎨 Main Dashboard**: http://localhost:3000
- **📡 Backend API**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs
- **🔍 Health Check**: http://localhost:8000/api/health

---

## 🎛️ **Features Overview**

### **🎨 Project Generator Tab**
- Enter project descriptions like "Create a todo app with React"
- AI generates complete projects with HTML, CSS, JavaScript, and Python files
- Real-time progress tracking

### **💬 Q&A Assistant Tab**
- Ask technical questions: "How do I use async/await in JavaScript?"
- Ask general questions: "What is machine learning?"
- Interactive chat interface with message history

### **📊 Workflow Monitor Tab**
- View real-time agent activity
- Track session history and performance metrics
- Monitor AI workflow progress

### **🎛️ Project Gallery Tab**
- Browse all generated projects
- Preview file contents
- Download and manage your creations

---

## 🐛 **Troubleshooting**

### **Port Already in Use**
```bash
# Kill processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### **Python Issues**
```bash
# Check Python version (should be 3.8+)
python3 --version

# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### **Node/Yarn Issues**
```bash
# Update Node and Yarn
brew upgrade node yarn

# Clear caches
yarn cache clean
npm cache clean --force

# Reinstall frontend dependencies
cd frontend
rm -rf node_modules package-lock.json yarn.lock
yarn install
```

### **Permission Issues**
```bash
# Fix npm/yarn permissions
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) ~/.yarn
```

### **Environment Variable Issues**
```bash
# Check if .env file exists and has content
cat .env

# Should show: GROQ_API_KEY=gsk_...
# If not, recreate it:
echo "GROQ_API_KEY=your_actual_key_here" > .env
```

---

## 🧪 **Testing Your Setup**

### **Test Backend Health**
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy","service":"Coder Buddy Dashboard"}
```

### **Test Q&A Functionality**
```bash
curl -X POST "http://localhost:8000/api/ask-question" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is Python?", "context": ""}'
```

### **Test Project Generation**
```bash
curl -X POST "http://localhost:8000/api/generate-project" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Create a simple HTML page"}'
```

---

## 🔧 **Manual Setup (If Scripts Don't Work)**

### **Install Prerequisites**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11+
brew install python@3.11

# Install Node.js and Yarn
brew install node yarn
```

### **Setup Python Environment**
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Setup Frontend**
```bash
cd frontend
yarn install
cd ..
```

### **Create Environment File**
```bash
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

---

## 📊 **Performance Expectations**

### **Response Times**
- **Q&A Questions**: 5-15 seconds
- **Project Generation**: 30-90 seconds
- **Page Loading**: 1-3 seconds

### **Resource Usage**
- **CPU**: High during AI processing (normal)
- **Memory**: ~500MB for both servers
- **Disk**: Generated projects stored in `generated_project/`

---

## 🆘 **Getting Help**

### **Common Success Indicators**
- ✅ Backend: "Application startup complete" message
- ✅ Frontend: "webpack compiled successfully" message  
- ✅ Browser: Colorful dashboard loads at localhost:3000

### **If Still Having Issues**
1. Run `python test_local_setup.py` to diagnose problems
2. Check that ports 3000 and 8000 are available
3. Ensure your Groq API key is valid and properly set in .env
4. Make sure you're using Python 3.8+ and Node.js 16+

---

## 🎉 **You're Ready!**

Once everything is set up, you'll have a beautiful AI-powered development assistant with:

- 🎨 **Stunning Web Interface** - Colorful, responsive, modern design
- 🤖 **Smart AI Agents** - Technical and general Q&A capabilities
- 🔧 **Project Generation** - Complete projects from natural language
- 📊 **Real-time Monitoring* - Track AI workflow progress
- 🎛️ **Project Management** - Browse and manage your creations

**Happy coding with your AI assistant! 🚀**