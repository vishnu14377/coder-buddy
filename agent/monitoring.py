"""
Monitoring utilities for tracking agent workflows and providing real-time updates.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
import queue

@dataclass
class WorkflowStep:
    agent_name: str
    step_name: str
    status: str  # 'running', 'completed', 'error'
    start_time: datetime
    end_time: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None

@dataclass
class WorkflowSession:
    session_id: str
    user_prompt: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = 'running'  # 'running', 'completed', 'error'
    steps: List[WorkflowStep] = None
    final_result: Optional[Any] = None
    
    def __post_init__(self):
        if self.steps is None:
            self.steps = []

class WorkflowMonitor:
    def __init__(self):
        self.sessions: Dict[str, WorkflowSession] = {}
        self.active_session_id: Optional[str] = None
        self.subscribers = []
        self.update_queue = queue.Queue()
        
    def start_session(self, session_id: str, user_prompt: str) -> WorkflowSession:
        """Start a new workflow session."""
        session = WorkflowSession(
            session_id=session_id,
            user_prompt=user_prompt,
            start_time=datetime.now()
        )
        self.sessions[session_id] = session
        self.active_session_id = session_id
        self._notify_subscribers('session_started', session)
        return session
    
    def start_step(self, agent_name: str, step_name: str) -> None:
        """Start a new step in the current session."""
        if not self.active_session_id:
            return
            
        session = self.sessions[self.active_session_id]
        step = WorkflowStep(
            agent_name=agent_name,
            step_name=step_name,
            status='running',
            start_time=datetime.now()
        )
        session.steps.append(step)
        self._notify_subscribers('step_started', {'session_id': self.active_session_id, 'step': step})
    
    def complete_step(self, result: Any = None) -> None:
        """Complete the current step."""
        if not self.active_session_id:
            return
            
        session = self.sessions[self.active_session_id]
        if session.steps:
            current_step = session.steps[-1]
            current_step.status = 'completed'
            current_step.end_time = datetime.now()
            current_step.result = result
            self._notify_subscribers('step_completed', {'session_id': self.active_session_id, 'step': current_step})
    
    def error_step(self, error: str) -> None:
        """Mark the current step as error."""
        if not self.active_session_id:
            return
            
        session = self.sessions[self.active_session_id]
        if session.steps:
            current_step = session.steps[-1]
            current_step.status = 'error'
            current_step.end_time = datetime.now()
            current_step.error = error
            self._notify_subscribers('step_error', {'session_id': self.active_session_id, 'step': current_step})
    
    def complete_session(self, final_result: Any = None) -> None:
        """Complete the current session."""
        if not self.active_session_id:
            return
            
        session = self.sessions[self.active_session_id]
        session.status = 'completed'
        session.end_time = datetime.now()
        session.final_result = final_result
        self._notify_subscribers('session_completed', session)
        self.active_session_id = None
    
    def error_session(self, error: str) -> None:
        """Mark the current session as error."""
        if not self.active_session_id:
            return
            
        session = self.sessions[self.active_session_id]
        session.status = 'error'
        session.end_time = datetime.now()
        self._notify_subscribers('session_error', {'session': session, 'error': error})
        self.active_session_id = None
    
    def get_session(self, session_id: str) -> Optional[WorkflowSession]:
        """Get a specific session."""
        return self.sessions.get(session_id)
    
    def get_recent_sessions(self, limit: int = 10) -> List[WorkflowSession]:
        """Get recent sessions."""
        sessions = list(self.sessions.values())
        sessions.sort(key=lambda x: x.start_time, reverse=True)
        return sessions[:limit]
    
    def subscribe(self, callback):
        """Subscribe to workflow updates."""
        self.subscribers.append(callback)
    
    def _notify_subscribers(self, event_type: str, data: Any):
        """Notify all subscribers of an event."""
        for callback in self.subscribers:
            try:
                callback(event_type, data)
            except Exception as e:
                print(f"Error notifying subscriber: {e}")
    
    def to_dict(self, session_id: str = None) -> Dict:
        """Convert session data to dictionary for JSON serialization."""
        if session_id:
            session = self.sessions.get(session_id)
            if session:
                return self._session_to_dict(session)
            return {}
        
        return {
            'sessions': {sid: self._session_to_dict(session) 
                        for sid, session in self.sessions.items()},
            'active_session_id': self.active_session_id
        }
    
    def _session_to_dict(self, session: WorkflowSession) -> Dict:
        """Convert a session to dictionary."""
        return {
            'session_id': session.session_id,
            'user_prompt': session.user_prompt,
            'start_time': session.start_time.isoformat() if session.start_time else None,
            'end_time': session.end_time.isoformat() if session.end_time else None,
            'status': session.status,
            'steps': [self._step_to_dict(step) for step in session.steps],
            'final_result': str(session.final_result) if session.final_result else None
        }
    
    def _step_to_dict(self, step: WorkflowStep) -> Dict:
        """Convert a step to dictionary."""
        return {
            'agent_name': step.agent_name,
            'step_name': step.step_name,
            'status': step.status,
            'start_time': step.start_time.isoformat() if step.start_time else None,
            'end_time': step.end_time.isoformat() if step.end_time else None,
            'result': str(step.result) if step.result else None,
            'error': step.error
        }

# Global monitor instance
workflow_monitor = WorkflowMonitor()