import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Monitor, 
  Activity, 
  Clock, 
  CheckCircle, 
  XCircle, 
  Loader2,
  Users,
  Zap,
  GitBranch,
  PlayCircle
} from 'lucide-react';

const WorkflowMonitor = () => {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    fetchSessions();
    const interval = setInterval(fetchSessions, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchSessions = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/sessions`);
      const data = await response.json();
      
      if (data.success) {
        setSessions(data.sessions);
        setLastUpdate(new Date());
      }
    } catch (error) {
      console.error('Failed to fetch sessions:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100';
      case 'running': return 'text-blue-600 bg-blue-100';
      case 'error': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return CheckCircle;
      case 'running': return Loader2;
      case 'error': return XCircle;
      default: return Clock;
    }
  };

  const formatTime = (timestamp) => {
    if (!timestamp) return 'N/A';
    return new Date(timestamp).toLocaleString();
  };

  const formatDuration = (start, end) => {
    if (!start) return 'N/A';
    const startTime = new Date(start);
    const endTime = end ? new Date(end) : new Date();
    const duration = Math.round((endTime - startTime) / 1000);
    
    if (duration < 60) return `${duration}s`;
    if (duration < 3600) return `${Math.floor(duration / 60)}m ${duration % 60}s`;
    return `${Math.floor(duration / 3600)}h ${Math.floor((duration % 3600) / 60)}m`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div 
        className="text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-green-100 to-blue-100 px-4 py-2 rounded-full mb-4">
          <Activity className="w-5 h-5 text-green-600" />
          <span className="text-green-700 font-medium">Workflow Monitor</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Real-time Agent Activity
        </h2>
        <p className="text-gray-600">
          Monitor your AI agents in action and track workflow progress
        </p>
      </motion.div>

      {/* Stats Cards */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-4 gap-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Sessions</p>
              <p className="text-2xl font-bold text-gray-900">{sessions.length}</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <GitBranch className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-green-600">
                {sessions.filter(s => s.status === 'completed').length}
              </p>
            </div>
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Running</p>
              <p className="text-2xl font-bold text-blue-600">
                {sessions.filter(s => s.status === 'running').length}
              </p>
            </div>
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Errors</p>
              <p className="text-2xl font-bold text-red-600">
                {sessions.filter(s => s.status === 'error').length}
              </p>
            </div>
            <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <XCircle className="w-6 h-6 text-red-600" />
            </div>
          </div>
        </div>
      </motion.div>

      {/* Sessions List */}
      <motion.div
        className="bg-white rounded-2xl shadow-xl border border-gray-100"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-semibold text-gray-900 flex items-center">
              <Monitor className="w-5 h-5 mr-2 text-blue-500" />
              Recent Sessions
            </h3>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Clock className="w-4 h-4" />
              <span>Last updated: {lastUpdate.toLocaleTimeString()}</span>
            </div>
          </div>
        </div>

        <div className="divide-y divide-gray-100">
          {isLoading ? (
            <div className="p-8 text-center">
              <Loader2 className="w-8 h-8 text-blue-500 animate-spin mx-auto mb-4" />
              <p className="text-gray-600">Loading sessions...</p>
            </div>
          ) : sessions.length === 0 ? (
            <div className="p-8 text-center">
              <Activity className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No sessions found</p>
              <p className="text-sm text-gray-500 mt-2">
                Sessions will appear here when you generate projects or ask questions
              </p>
            </div>
          ) : (
            sessions.map((session) => {
              const StatusIcon = getStatusIcon(session.status);
              
              return (
                <motion.div
                  key={session.session_id}
                  className="p-6 hover:bg-gray-50 cursor-pointer transition-colors"
                  onClick={() => setSelectedSession(
                    selectedSession?.session_id === session.session_id ? null : session
                  )}
                  whileHover={{ x: 4 }}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <StatusIcon className={`w-5 h-5 ${
                          session.status === 'running' ? 'animate-spin' : ''
                        } ${getStatusColor(session.status).split(' ')[0]}`} />
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(session.status)}`}>
                          {session.status.toUpperCase()}
                        </span>
                        <span className="text-sm text-gray-500">
                          {session.session_id.slice(0, 8)}...
                        </span>
                      </div>
                      
                      <h4 className="text-lg font-medium text-gray-900 mb-1">
                        {session.user_prompt.length > 80 
                          ? `${session.user_prompt.slice(0, 80)}...` 
                          : session.user_prompt
                        }
                      </h4>
                      
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span className="flex items-center space-x-1">
                          <PlayCircle className="w-4 h-4" />
                          <span>Started: {formatTime(session.start_time)}</span>
                        </span>
                        <span className="flex items-center space-x-1">
                          <Clock className="w-4 h-4" />
                          <span>Duration: {formatDuration(session.start_time, session.end_time)}</span>
                        </span>
                        {session.steps && (
                          <span className="flex items-center space-x-1">
                            <Users className="w-4 h-4" />
                            <span>Steps: {session.steps.length}</span>
                          </span>
                        )}
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <Zap className="w-5 h-5 text-purple-500" />
                    </div>
                  </div>

                  {/* Expanded Session Details */}
                  {selectedSession?.session_id === session.session_id && (
                    <motion.div
                      className="mt-4 p-4 bg-gray-50 rounded-lg"
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                    >
                      <h5 className="font-medium text-gray-900 mb-3">Workflow Steps</h5>
                      {session.steps && session.steps.length > 0 ? (
                        <div className="space-y-2">
                          {session.steps.map((step, index) => {
                            const StepIcon = getStatusIcon(step.status);
                            return (
                              <div key={index} className="flex items-center space-x-3 p-2 bg-white rounded border">
                                <StepIcon className={`w-4 h-4 ${
                                  step.status === 'running' ? 'animate-spin' : ''
                                } ${getStatusColor(step.status).split(' ')[0]}`} />
                                <div className="flex-1">
                                  <p className="text-sm font-medium text-gray-800">
                                    {step.agent_name} - {step.step_name}
                                  </p>
                                  <p className="text-xs text-gray-500">
                                    {formatDuration(step.start_time, step.end_time)}
                                  </p>
                                </div>
                                <span className={`px-2 py-1 rounded text-xs ${getStatusColor(step.status)}`}>
                                  {step.status}
                                </span>
                              </div>
                            );
                          })}
                        </div>
                      ) : (
                        <p className="text-sm text-gray-500">No steps recorded</p>
                      )}
                    </motion.div>
                  )}
                </motion.div>
              );
            })
          )}
        </div>
      </motion.div>
    </div>
  );
};

export default WorkflowMonitor;