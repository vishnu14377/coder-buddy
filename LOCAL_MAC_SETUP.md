# 🍎 Coder Buddy - Local Mac Setup Guide

## 📋 **Prerequisites**

### 1. **Install Homebrew** (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. **Install Python 3.11+**
```bash
brew install python@3.11
python3 --version  # Should show 3.11+
```

### 3. **Install Node.js and Yarn**
```bash
brew install node yarn
node --version  # Should show 18+
yarn --version  # Should show 1.22+
```

### 4. **Install UV Package Manager**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Add to PATH (add to ~/.zshrc or ~/.bash_profile)
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
uv --version
```

---

## 🚀 **Project Setup**

### **Step 1: Clone/Download Project**
```bash
# If you have the project files, navigate to the directory
cd /path/to/coder-buddy

# Or create the directory structure if starting fresh
mkdir coder-buddy && cd coder-buddy
```

### **Step 2: Create Python Virtual Environment**
```bash
# Create virtual environment using UV
uv venv
source .venv/bin/activate

# Verify virtual environment is active
which python  # Should show path with .venv
```

### **Step 3: Install Python Dependencies**
```bash
# Install core dependencies
pip install langchain langchain-core langchain-google-genai langgraph pydantic python-dotenv fastapi uvicorn websockets framer-motion

# Or if you have requirements file
pip install -r requirements.txt
```

### **Step 4: Install Frontend Dependencies**
```bash
# Navigate to frontend directory
cd frontend

# Install React dependencies
yarn install

# Go back to root
cd ..
```

### **Step 5: Environment Configuration**
```bash
# Create .env file in root directory
touch .env

# Add your Google API key (get from https://aistudio.google.com/app/apikey)
echo "GOOGLE_API_KEY=your_google_api_key_here" >> .env
```

---

## 🎯 **Running the Application**

### **Option 1: Automated Startup (Recommended)**
```bash
# Make sure you're in the root directory with virtual environment active
source .venv/bin/activate
python start_dashboard.py
```

### **Option 2: Manual Startup**

**Terminal 1 - Backend Server:**
```bash
source .venv/bin/activate
python -m uvicorn web_server:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 - Frontend Server:**
```bash
cd frontend
yarn start
```

### **Option 3: VSCode Integrated Terminals**

1. Open VSCode in the project directory
2. Open Terminal in VSCode (`Terminal` → `New Terminal`)
3. Split terminal (`Terminal` → `Split Terminal`)

**Terminal 1 (Backend):**
```bash
source .venv/bin/activate
python -m uvicorn web_server:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
yarn start
```

---

## 🌐 **Access Points**

Once both servers are running:

- **🎨 Frontend Dashboard**: http://localhost:3000
- **📡 Backend API**: http://localhost:8000
- **📚 API Docs**: http://localhost:8000/docs

---

## 🐛 **Troubleshooting Common Mac Issues**

### **Issue 1: Python Version Conflicts**
```bash
# Check Python version
python3 --version

# If using wrong version, create alias
echo 'alias python=python3' >> ~/.zshrc
source ~/.zshrc
```

### **Issue 2: Node/Yarn Issues**
```bash
# Update Node and Yarn
brew upgrade node yarn

# Clear yarn cache if needed
yarn cache clean
```

### **Issue 3: Permission Issues**
```bash
# Fix npm/yarn permissions
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) ~/.yarn
```

### **Issue 4: Port Already in Use**
```bash
# Kill processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### **Issue 5: Virtual Environment Issues**
```bash
# Remove and recreate virtual environment
rm -rf .venv
uv venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🔧 **VSCode Configuration**

### **Recommended Extensions:**
- Python
- Pylance
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Thunder Client (for API testing)

### **VSCode Settings (create .vscode/settings.json):**
```json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "eslint.workingDirectories": ["frontend"],
    "emmet.includeLanguages": {
        "javascript": "javascriptreact"
    }
}
```

### **Launch Configuration (create .vscode/launch.json):**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/.venv/bin/uvicorn",
            "args": ["web_server:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

---

## ✅ **Verification Steps**

### **1. Test Backend Health**
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy","service":"Coder Buddy Dashboard"}
```

### **2. Test Q&A Functionality**
```bash
curl -X POST "http://localhost:8000/api/ask-question" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is Python?", "context": ""}'
```

### **3. Test Frontend Loading**
Open http://localhost:3000 in your browser - you should see the colorful Coder Buddy dashboard.

---

## 🎯 **Quick Start Commands Summary**

```bash
# 1. Setup (one-time)
uv venv && source .venv/bin/activate
pip install groq langchain langchain-core langchain-groq langgraph pydantic python-dotenv fastapi uvicorn websockets
cd frontend && yarn install && cd ..
echo "GROQ_API_KEY=your_key_here" > .env

# 2. Run (every time)
# Terminal 1:
source .venv/bin/activate && python -m uvicorn web_server:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2:
cd frontend && yarn start
```

---

## 🆘 **Still Having Issues?**

If you encounter any problems:

1. **Check Python Virtual Environment**: `which python` should show `.venv/bin/python`
2. **Verify Dependencies**: `pip list` should show all required packages
3. **Check Node Version**: `node --version` should be 18+
4. **Verify Ports**: Make sure ports 3000 and 8000 are available
5. **Check Logs**: Look at terminal output for specific error messages

**Common Success Indicators:**
- Backend: "Application startup complete" message
- Frontend: "webpack compiled successfully" message
- Browser: Colorful dashboard loads at localhost:3000