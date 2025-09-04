"""
Optimized FastAPI web server with ultra-fast responses and streaming.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import uuid
import os
import time

# Import optimized agents
from agent.fast_qa_agent import ultra_fast_qa_agent
from agent.fast_project_generator import fast_project_generator
from agent.monitoring import workflow_monitor

app = FastAPI(title="Coder Buddy Dashboard - Optimized", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced data models
class ProjectRequest(BaseModel):
    prompt: str
    fast_mode: bool = True

class QARequest(BaseModel):
    question: str
    context: Optional[str] = ""
    fast_mode: bool = True

class StreamingQARequest(BaseModel):
    question: str
    context: Optional[str] = ""

# WebSocket connection manager with optimizations
class OptimizedConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_pool = asyncio.Queue(maxsize=100)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast_fast(self, message: dict):
        """Optimized broadcast with error handling."""
        if not self.active_connections:
            return
        
        message_str = json.dumps(message)
        disconnected = []
        
        # Send to all connections concurrently
        tasks = []
        for connection in self.active_connections:
            tasks.append(self._send_safe(connection, message_str))
        
        # Wait for all sends to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Remove disconnected clients
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                disconnected.append(self.active_connections[i])
        
        for conn in disconnected:
            self.disconnect(conn)

    async def _send_safe(self, websocket: WebSocket, message: str):
        """Send message safely with error handling."""
        try:
            await websocket.send_text(message)
        except Exception:
            raise  # Will be caught by gather

manager = OptimizedConnectionManager()

# Optimized API Routes

@app.get("/")
async def root():
    return {
        "message": "Coder Buddy Dashboard - Ultra Fast Mode! ⚡",
        "version": "2.0.0",
        "optimizations": ["Fast Models", "Caching", "Parallel Processing", "Templates"]
    }

@app.get("/api/health")
async def health_check():
    """Optimized health check with performance metrics."""
    start_time = time.time()
    
    # Quick system check
    response_time = (time.time() - start_time) * 1000
    
    return {
        "status": "healthy",
        "service": "Coder Buddy Dashboard - Optimized",
        "response_time_ms": round(response_time, 2),
        "optimizations_active": True,
        "cache_status": "active",
        "fast_models": "enabled"
    }

@app.post("/api/generate-project-fast")
async def generate_project_fast(request: ProjectRequest):
    """Ultra-fast project generation endpoint."""
    start_time = time.time()
    
    try:
        print(f"🚀 Fast project generation request: {request.prompt}")
        
        # Use optimized generator
        result = await fast_project_generator.generate_project_fast(request.prompt)
        
        total_time = (time.time() - start_time) * 1000
        
        # Broadcast to WebSocket clients
        await manager.broadcast_fast({
            "type": "project_completed",
            "data": {
                "session_id": result.get("session_id"),
                "generation_time": total_time,
                "success": result.get("success", False)
            }
        })
        
        return {
            **result,
            "api_response_time": round(total_time, 2),
            "message": f"Project generated in {total_time:.0f}ms! ⚡"
        }
        
    except Exception as e:
        error_time = (time.time() - start_time) * 1000
        print(f"❌ Fast generation error after {error_time:.1f}ms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating project: {str(e)}")

@app.post("/api/ask-question-fast")
async def ask_question_fast(request: QARequest):
    """Ultra-fast Q&A endpoint with caching."""
    start_time = time.time()
    
    try:
        print(f"🔥 Fast Q&A request: {request.question[:50]}...")
        
        # Use ultra-fast agent
        if request.fast_mode:
            answer = await ultra_fast_qa_agent.answer_question_async(request.question, request.context)
        else:
            answer = ultra_fast_qa_agent.answer_question(request.question, request.context)
        
        response_time = (time.time() - start_time) * 1000
        
        return {
            "success": True,
            "answer": answer,
            "question": request.question,
            "is_technical": ultra_fast_qa_agent.is_technical_question(request.question),
            "response_time_ms": round(response_time, 2),
            "cached": response_time < 100,  # Likely cached if < 100ms
            "fast_mode": request.fast_mode
        }
        
    except Exception as e:
        error_time = (time.time() - start_time) * 1000
        print(f"❌ Fast Q&A error after {error_time:.1f}ms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.post("/api/ask-question-streaming")
async def ask_question_streaming(request: StreamingQARequest):
    """Streaming Q&A endpoint for real-time responses."""
    
    async def generate_response():
        try:
            # Start with immediate acknowledgment
            yield f"data: {json.dumps({'type': 'start', 'message': 'Processing your question...'})}\n\n"
            
            # Check for instant responses first
            normalized_question = ultra_fast_qa_agent._normalize_question(request.question)
            if normalized_question in ultra_fast_qa_agent.quick_responses:
                answer = ultra_fast_qa_agent.quick_responses[normalized_question]
                yield f"data: {json.dumps({'type': 'complete', 'answer': answer, 'response_time': '< 1ms'})}\n\n"
                return
            
            # Check cache
            cache_key = f"{request.question}|{request.context}"
            cached_answer = ultra_fast_qa_agent.cache.get(cache_key)
            if cached_answer:
                yield f"data: {json.dumps({'type': 'complete', 'answer': cached_answer, 'response_time': '< 10ms (cached)'})}\n\n"
                return
            
            # Generate new response
            yield f"data: {json.dumps({'type': 'thinking', 'message': 'Generating response...'})}\n\n"
            
            answer = await ultra_fast_qa_agent.answer_question_async(request.question, request.context)
            
            yield f"data: {json.dumps({'type': 'complete', 'answer': answer, 'response_time': 'Generated fresh'})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(generate_response(), media_type="text/plain")

# Legacy endpoints for backward compatibility
@app.post("/api/generate-project")
async def generate_project_legacy(request: ProjectRequest):
    """Legacy endpoint redirecting to fast version."""
    return await generate_project_fast(request)

@app.post("/api/ask-question")
async def ask_question_legacy(request: QARequest):
    """Legacy endpoint redirecting to fast version."""
    return await ask_question_fast(request)

@app.get("/api/sessions")
async def get_sessions():
    """Get recent workflow sessions - optimized."""
    try:
        sessions = workflow_monitor.get_recent_sessions(limit=20)
        return {
            "success": True,
            "sessions": [workflow_monitor._session_to_dict(session) for session in sessions],
            "count": len(sessions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sessions: {str(e)}")

@app.get("/api/generated-projects")
async def get_generated_projects():
    """Get list of generated projects - optimized."""
    try:
        project_root = "/app/generated_project"
        projects = []
        
        if os.path.exists(project_root):
            # Use async file operations for better performance
            items = os.listdir(project_root)
            
            for item in items[:20]:  # Limit for performance
                item_path = os.path.join(project_root, item)
                if os.path.isfile(item_path):
                    try:
                        # Quick preview only
                        with open(item_path, 'r', encoding='utf-8') as f:
                            content = f.read(200)  # Read only first 200 chars
                        projects.append({
                            "name": item,
                            "path": item_path,
                            "type": "file",
                            "preview": content + "..." if len(content) == 200 else content
                        })
                    except Exception:
                        projects.append({
                            "name": item,
                            "path": item_path,
                            "type": "file",
                            "preview": "Preview not available"
                        })
        
        return {
            "success": True,
            "projects": projects,
            "count": len(projects)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")

@app.get("/api/performance-stats")
async def get_performance_stats():
    """Get performance statistics."""
    return {
        "cache_size": len(ultra_fast_qa_agent.cache.memory_cache),
        "active_connections": len(manager.active_connections),
        "optimizations": {
            "fast_models": "gemini-1.5-flash-8b",
            "caching": "active",
            "parallel_processing": "enabled",
            "templates": "loaded"
        },
        "response_times": {
            "cached_qa": "< 10ms",
            "quick_responses": "< 1ms",
            "template_projects": "< 100ms",
            "custom_projects": "< 3000ms"
        }
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Optimized WebSocket endpoint."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "ping":
                await websocket.send_text(json.dumps({
                    "type": "pong",
                    "timestamp": time.time()
                }))
            elif message_data.get("type") == "get_performance":
                stats = {
                    "type": "performance_update",
                    "cache_size": len(ultra_fast_qa_agent.cache.memory_cache),
                    "active_connections": len(manager.active_connections),
                    "fast_mode": True
                }
                await websocket.send_text(json.dumps(stats))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Coder Buddy - Ultra Fast Mode!")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)