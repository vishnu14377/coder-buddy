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

from agent.graph import route_request, agent, qa_agent_compiled
from agent.monitoring import workflow_monitor
from agent.qa_agent import qa_agent

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
    """Generate a new project using the agent workflow."""
    try:
        # Run the project generation workflow
        result = route_request(request.prompt, "project")
        
        # Extract useful information from the result
        session_info = {}
        if 'session_id' in result:
            session_info = workflow_monitor.to_dict(result['session_id'])
        
        return {
            "success": True,
            "result": str(result),
            "session_info": session_info,
            "message": "Project generation completed successfully!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating project: {str(e)}")

@app.post("/api/ask-question")
async def ask_question(request: QARequest):
    """Ask a question to the general Q&A agent."""
    try:
        # Use the Q&A agent directly for faster response
        answer = qa_agent.answer_question(request.question, request.context)
        
        return {
            "success": True,
            "answer": answer,
            "question": request.question,
            "is_technical": qa_agent.is_technical_question(request.question)
        }
    except Exception as e:
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
    """Get list of generated projects."""
    try:
        project_root = "/app/generated_project"
        projects = []
        
        if os.path.exists(project_root):
            for item in os.listdir(project_root):
                item_path = os.path.join(project_root, item)
                if os.path.isfile(item_path):
                    # Read file content for preview
                    try:
                        with open(item_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        projects.append({
                            "name": item,
                            "path": item_path,
                            "type": "file",
                            "preview": content[:500] + "..." if len(content) > 500 else content
                        })
                    except Exception:
                        projects.append({
                            "name": item,
                            "path": item_path,
                            "type": "file",
                            "preview": "Could not read file content"
                        })
                elif os.path.isdir(item_path):
                    # List directory contents
                    try:
                        files = os.listdir(item_path)
                        projects.append({
                            "name": item,
                            "path": item_path,
                            "type": "directory",
                            "files": files
                        })
                    except Exception:
                        projects.append({
                            "name": item,
                            "path": item_path,
                            "type": "directory",
                            "files": []
                        })
        
        return {
            "success": True,
            "projects": projects
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")

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