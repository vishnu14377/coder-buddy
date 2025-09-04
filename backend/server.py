"""
FastAPI web server for Coder Buddy dashboard and Q&A interface.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import uuid
import os
import time

from agent.graph import route_request, agent, qa_agent_compiled
from agent.monitoring import workflow_monitor
from agent.qa_agent import qa_agent
# Import INSTANT generators
from agent.fast_qa_agent import ultra_fast_qa_agent
from agent.instant_generator import instant_generator

app = FastAPI(title="Coder Buddy Dashboard", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ProjectRequest(BaseModel):
    prompt: str

class QARequest(BaseModel):
    question: str
    context: Optional[str] = ""

class ChatMessage(BaseModel):
    message: str
    type: str  # 'user' or 'assistant'
    timestamp: str

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# API Routes

@app.get("/")
async def root():
    return {"message": "Coder Buddy Dashboard API is running!"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Coder Buddy Dashboard"}

@app.post("/api/generate-project")
async def generate_project(request: ProjectRequest):
    """Generate project INSTANTLY using pre-built templates."""
    start_time = time.time()
    
    try:
        print(f"⚡ INSTANT project generation: {request.prompt}")
        
        # Use instant generator for sub-second generation
        result = instant_generator.generate_instant(request.prompt)
        
        total_time = (time.time() - start_time) * 1000
        
        return {
            **result,
            "api_response_time": round(total_time, 2),
            "message": f"⚡ INSTANT: Project generated in {result.get('generation_time', 0):.0f}ms!",
            "optimized": True,
            "instant": True
        }
        
    except Exception as e:
        error_time = (time.time() - start_time) * 1000
        print(f"❌ Instant generation error after {error_time:.1f}ms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating project: {str(e)}")

@app.post("/api/ask-question")
async def ask_question(request: QARequest):
    """Ask a question using ultra-fast Q&A agent."""
    start_time = time.time()
    
    try:
        # Use ultra-fast agent with async processing
        answer = await ultra_fast_qa_agent.answer_question_async(request.question, request.context)
        
        response_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "answer": answer,
            "question": request.question,
            "is_technical": ultra_fast_qa_agent.is_technical_question(request.question),
            "response_time_ms": round(response_time, 2),
            "optimized": True
        }
    except Exception as e:
        error_time = (time.time() - start_time) * 1000
        print(f"❌ Q&A error after {error_time:.1f}ms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/api/sessions")
async def get_sessions():
    """Get recent workflow sessions."""
    try:
        sessions = workflow_monitor.get_recent_sessions(limit=20)
        return {
            "success": True,
            "sessions": [workflow_monitor._session_to_dict(session) for session in sessions]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sessions: {str(e)}")

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get details of a specific session."""
    try:
        session_data = workflow_monitor.to_dict(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {
            "success": True,
            "session": session_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching session: {str(e)}")

@app.get("/api/generated-projects")
async def get_generated_projects():
    """Get list of generated projects with enhanced details."""
    try:
        project_root = "/app/generated_project"
        projects = []
        
        if os.path.exists(project_root):
            for item in os.listdir(project_root):
                item_path = os.path.join(project_root, item)
                if os.path.isfile(item_path):
                    try:
                        # Get file preview
                        with open(item_path, 'r', encoding='utf-8') as f:
                            content = f.read(300)  # First 300 chars
                        
                        # Determine file type
                        file_type = "unknown"
                        if item.endswith('.html'):
                            file_type = "HTML"
                        elif item.endswith('.css'):
                            file_type = "CSS"
                        elif item.endswith('.js'):
                            file_type = "JavaScript"
                        elif item.endswith('.py'):
                            file_type = "Python"
                        
                        projects.append({
                            "name": item,
                            "path": item_path,
                            "type": file_type,
                            "preview": content + ("..." if len(content) == 300 else ""),
                            "size": os.path.getsize(item_path),
                            "modified": os.path.getmtime(item_path)
                        })
                    except Exception:
                        projects.append({
                            "name": item,
                            "path": item_path,
                            "type": "unknown",
                            "preview": "Preview not available",
                            "size": 0,
                            "modified": 0
                        })
        
        return {
            "success": True,
            "projects": projects,
            "count": len(projects)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")

@app.get("/api/file-content")
async def get_file_content(path: str):
    """Get content of a specific file."""
    try:
        # Security check - ensure path is within project directory
        if not path.startswith("/app/generated_project/"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="File not found")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "content": content,
            "path": path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

@app.post("/api/save-file")
async def save_file(request: dict):
    """Save content to a specific file."""
    try:
        path = request.get("path")
        content = request.get("content")
        
        if not path or content is None:
            raise HTTPException(status_code=400, detail="Path and content are required")
        
        # Security check - ensure path is within project directory
        if not path.startswith("/app/generated_project/"):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "message": "File saved successfully",
            "path": path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
            elif message_data.get("type") == "get_status":
                # Send current workflow status
                status = {
                    "type": "status_update",
                    "active_session": workflow_monitor.active_session_id,
                    "recent_sessions": len(workflow_monitor.sessions)
                }
                await websocket.send_text(json.dumps(status))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Set up workflow monitor callback for real-time updates
def workflow_callback(event_type: str, data: Any):
    """Callback for workflow events to send real-time updates."""
    message = {
        "type": "workflow_update",
        "event": event_type,
        "data": str(data)  # Convert to string for JSON serialization
    }
    
    # Send to all connected WebSocket clients
    asyncio.create_task(manager.broadcast(json.dumps(message)))

workflow_monitor.subscribe(workflow_callback)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)