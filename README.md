# 🛠️ Coder Buddy - Enhanced AI Development Assistant

**Coder Buddy** is a comprehensive AI-powered coding assistant built with [LangGraph](https://github.com/langchain-ai/langgraph). It features a multi-agent development team that can transform natural language requests into complete, working projects AND answer general questions with an enhanced production-level web interface.

## 🆕 NEW FEATURES

### ✨ **Production-Level Web Dashboard**
- **Modern React Frontend** - Beautiful, colorful, and engaging user interface
- **Real-time Workflow Monitoring** - Track your AI agents in action
- **Interactive Q&A Chat** - Get help with both technical and general questions
- **Project Gallery** - Browse and explore generated projects
- **WebSocket Integration** - Real-time updates and notifications

### 🤖 **Enhanced Agent System**
- **General Q&A Agent** - Comprehensive assistant for technical AND general knowledge
- **Intelligent Request Routing** - Automatically detects project requests vs questions
- **Enhanced Monitoring** - Track agent performance and session history
- **Session Management** - Persistent workflow tracking

---

## 🏗️ Architecture

### **Multi-Agent Development Team**
- **Planner Agent** – Analyzes your request and generates a detailed project plan
- **Architect Agent** – Breaks down the plan into specific engineering tasks
- **Coder Agent** – Implements each task and writes directly into files
- **Q&A Agent** – Handles both technical programming and general knowledge questions

### **Web Dashboard Components**
- **Project Generator** – Create projects through intuitive web interface
- **Q&A Chat** – Interactive chat with AI assistant
- **Workflow Monitor** – Real-time agent activity tracking
- **Project Gallery** – Browse generated projects with preview capabilities

<div style="text-align: center;">
    <img src="resources/coder_buddy_diagram.png" alt="Enhanced Coder Agent Architecture" width="90%"/>
</div>

---

## 🚀 Getting Started

### Prerequisites
- **uv package manager** - Follow instructions [here](https://docs.astral.sh/uv/getting-started/installation/)
- **Node.js & Yarn** - For the React frontend
- **Google API Key** - Create one [here](https://aistudio.google.com/app/apikey)

### ⚙️ Installation and Setup

1. **Clone and Setup Environment**
   ```bash
   cd /path/to/coder-buddy
   uv venv && source .venv/bin/activate
   ```

2. **Install Python Dependencies**
   ```bash
   python -m pip install langchain langchain-core langchain-google-genai langgraph pydantic python-dotenv fastapi uvicorn websockets
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd frontend
   yarn install
   ```

4. **Configure Environment**
   ```bash
   # Create .env file in root directory
   echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
   ```

---

## 🎯 Usage Options

### Option 1: **Web Dashboard (Recommended)**

Start both backend and frontend servers:

```bash
# Option A: Use the startup script
python start_dashboard.py

# Option B: Start manually
# Terminal 1 - Backend
python -m uvicorn web_server:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend  
cd frontend && yarn start
```

**Access Points:**
- 🌐 **Frontend Dashboard**: http://localhost:3000
- 📡 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs

### Option 2: **Enhanced CLI**

```bash
# Interactive CLI with smart routing
python main.py

# Show web dashboard option
python main.py --web
```

---

## 🌟 Features & Capabilities

### **🎨 Project Generation**
- **Natural Language Input** - Describe your project idea in plain English
- **Multi-Agent Processing** - Planner → Architect → Coder workflow
- **Real-time Monitoring** - Watch agents work on your project
- **File Management** - Automatic project structure creation

**Example Prompts:**
- "Create a modern todo app with React and local storage"
- "Build a colorful weather dashboard with animations"
- "Make a creative portfolio website with gradient backgrounds"

### **💬 General Q&A Assistant**
- **Technical Questions** - Programming help, syntax, best practices
- **General Knowledge** - Wide range of topics and information
- **Interactive Chat** - Conversational interface with history
- **Smart Detection** - Automatically categorizes technical vs general questions

**Example Questions:**
- "How do I implement authentication in React?"
- "What's the difference between Python and JavaScript?"
- "Explain machine learning in simple terms"

### **📊 Workflow Monitoring**
- **Session Tracking** - Monitor all agent activities
- **Real-time Updates** - Live progress tracking
- **Performance Metrics** - Success rates and timing
- **Historical Data** - Browse past sessions and results

### **🎛️ Project Gallery**
- **Generated Projects** - Browse all created projects
- **File Preview** - View file contents and structure
- **Project Management** - Organize and access your creations
- **Download Options** - Export projects for use

---

## 🎨 Web Interface Features

### **Modern Design System**
- **Colorful & Creative** - Vibrant, engaging interface
- **Responsive Design** - Works on all screen sizes
- **Smooth Animations** - Framer Motion powered interactions
- **Glass Morphism** - Modern UI/UX patterns

### **Real-time Capabilities**
- **WebSocket Integration** - Live updates and notifications
- **Progress Tracking** - Watch agents work in real-time
- **Session Management** - Persistent state across interactions
- **Error Handling** - Graceful error recovery and reporting

---

## 🧪 Example Use Cases

### **Web Development**
```
Create a modern blog website with:
- Responsive design
- Dark/light theme toggle
- Comment system
- Search functionality
```

### **Data Analysis**
```
Build a data visualization dashboard with:
- Interactive charts
- CSV file upload
- Statistical analysis
- Export capabilities
```

### **Q&A Examples**
- **Technical**: "How do I optimize React component performance?"
- **General**: "What are the benefits of sustainable energy?"
- **Mixed**: "Explain the concept of cloud computing and its applications"

---

## 🔧 API Endpoints

### **Backend API (Port 8000)**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/generate-project` | POST | Generate a new project |
| `/api/ask-question` | POST | Ask Q&A agent |
| `/api/sessions` | GET | Get workflow sessions |
| `/api/sessions/{id}` | GET | Get specific session |
| `/api/generated-projects` | GET | List generated projects |
| `/ws` | WebSocket | Real-time updates |

### **Request Examples**

```bash
# Generate Project
curl -X POST "http://localhost:8000/api/generate-project" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Create a todo app with HTML, CSS, JavaScript"}'

# Ask Question
curl -X POST "http://localhost:8000/api/ask-question" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is React?", "context": ""}'
```

---

## 🔄 Workflow Process

### **Project Generation Flow**
1. **User Input** → Natural language project description
2. **Planner** → Analyzes requirements and creates structured plan
3. **Architect** → Breaks down into implementation tasks
4. **Coder** → Executes tasks and creates files
5. **Monitoring** → Tracks progress and reports completion

### **Q&A Flow**
1. **Question Input** → User asks technical or general question
2. **Classification** → System determines question type
3. **Processing** → AI generates comprehensive answer
4. **Response** → Formatted answer with context

---

## 🎯 Best Practices

### **For Project Generation**
- Be specific about features and requirements
- Mention preferred technologies or frameworks
- Include styling preferences (modern, colorful, minimal)
- Specify any special functionality needed

### **For Q&A**
- Ask clear, specific questions
- Provide context when helpful
- Use follow-up questions for clarification
- Explore both technical and general topics

---

## 🛠️ Development & Customization

### **Adding New Features**
- **Frontend Components** - Located in `/frontend/src/components/`
- **Backend Endpoints** - Add to `web_server.py`
- **Agent Logic** - Extend `agent/graph.py`
- **Monitoring** - Enhance `agent/monitoring.py`

### **Styling Customization**
- **Tailwind Config** - `frontend/tailwind.config.js`
- **Custom CSS** - `frontend/src/App.css`
- **Component Styles** - Individual component files

---

## 📊 Performance & Monitoring

### **System Requirements**
- **Memory**: 2GB RAM minimum (4GB recommended)
- **CPU**: Multi-core processor recommended
- **Storage**: Projects stored in `/generated_project/`
- **Network**: Internet connection for AI model access

### **Monitoring Features**
- **Real-time Metrics** - Agent performance tracking
- **Session History** - Complete workflow logs
- **Error Tracking** - Comprehensive error reporting
- **Resource Usage** - System performance monitoring

---

## 🚀 Production Deployment

### **Environment Setup**
```bash
# Production environment variables
GOOGLE_API_KEY=your_production_key
NODE_ENV=production
REACT_APP_BACKEND_URL=https://your-domain.com/api
```

### **Docker Deployment**
```dockerfile
# Example Dockerfile structure
FROM node:18 as frontend-build
# ... frontend build steps

FROM python:3.11
# ... backend setup
COPY --from=frontend-build /app/build ./frontend/build
```

---

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create feature branch
3. Install dependencies
4. Make changes
5. Test thoroughly
6. Submit pull request

### **Code Standards**
- **Python**: Follow PEP 8 standards
- **JavaScript**: Use ESLint configuration
- **React**: Functional components with hooks
- **CSS**: Tailwind-first approach

---

## 📝 License

Copyright©️ Codebasics Inc. All rights reserved.

---

## 🎉 What's New in This Version

### **🆕 Major Enhancements**
- ✅ **Production-level Web Interface** with React dashboard
- ✅ **General Q&A Agent** for comprehensive assistance
- ✅ **Real-time Monitoring** with WebSocket integration
- ✅ **Enhanced UI/UX** with colorful, engaging design
- ✅ **Project Gallery** with file preview capabilities
- ✅ **Session Management** for workflow tracking
- ✅ **API Integration** for seamless frontend-backend communication

### **🔄 Improvements**
- Enhanced error handling and recovery
- Improved agent coordination and monitoring
- Better file organization and project structure
- Responsive design for all screen sizes
- Performance optimizations for better user experience

The enhanced Coder Buddy now provides a complete development assistant experience with both powerful AI capabilities and a beautiful, intuitive interface! 🚀