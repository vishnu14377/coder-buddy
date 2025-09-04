import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Code2, 
  MessageCircle, 
  Sparkles, 
  Cpu, 
  Palette, 
  Zap,
  Monitor,
  GitBranch,
  Settings
} from 'lucide-react';
import './App.css';

// Import components
import ProjectGenerator from './components/ProjectGenerator';
import EnhancedQAChat from './components/EnhancedQAChat';
import WorkflowMonitor from './components/WorkflowMonitor';
import EnhancedProjectGallery from './components/EnhancedProjectGallery';
import PerformanceMonitor from './components/PerformanceMonitor';

function App() {
  const [activeTab, setActiveTab] = useState('generate');
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Check API connection
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const response = await fetch('/api/health');
      if (response.ok) {
        setIsConnected(true);
      }
    } catch (error) {
      console.error('Connection check failed:', error);
      setIsConnected(false);
    }
  };

  const tabs = [
    { id: 'generate', label: 'Generate Project', icon: Code2, color: 'primary' },
    { id: 'chat', label: 'Q&A Assistant', icon: MessageCircle, color: 'secondary' },
    { id: 'performance', label: 'Performance', icon: Zap, color: 'accent' },
    { id: 'monitor', label: 'Workflow Monitor', icon: Monitor, color: 'accent' },
    { id: 'gallery', label: 'Project Gallery', icon: GitBranch, color: 'primary' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <motion.div 
              className="flex items-center space-x-3"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="relative">
                <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-600 rounded-xl flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-400 rounded-full animate-pulse"></div>
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                  Coder Buddy
                </h1>
                <p className="text-sm text-gray-500">AI-Powered Development Assistant</p>
              </div>
            </motion.div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 px-3 py-1 rounded-full text-sm bg-yellow-100 text-yellow-700">
                <Zap className="w-3 h-3 animate-pulse" />
                <span>Ultra Fast Mode</span>
              </div>
              <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
                isConnected 
                  ? 'bg-green-100 text-green-700' 
                  : 'bg-red-100 text-red-700'
              }`}>
                <div className={`w-2 h-2 rounded-full ${
                  isConnected ? 'bg-green-500' : 'bg-red-500'
                } animate-pulse`}></div>
                <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white/60 backdrop-blur-sm border-b border-gray-200/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8 overflow-x-auto">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              
              return (
                <motion.button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 px-4 py-4 border-b-2 font-medium text-sm transition-all ${
                    isActive
                      ? `border-${tab.color}-500 text-${tab.color}-600`
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                  whileHover={{ y: -2 }}
                  whileTap={{ y: 0 }}
                >
                  <Icon className={`w-5 h-5 ${
                    isActive ? `text-${tab.color}-500` : 'text-gray-400'
                  }`} />
                  <span>{tab.label}</span>
                </motion.button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="animate-fadeInUp"
        >
          {activeTab === 'generate' && <ProjectGenerator />}
          {activeTab === 'chat' && <EnhancedQAChat />}
          {activeTab === 'performance' && <PerformanceMonitor />}
          {activeTab === 'monitor' && <WorkflowMonitor />}
          {activeTab === 'gallery' && <EnhancedProjectGallery />}
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="bg-white/40 backdrop-blur-sm border-t border-gray-200/50 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <Cpu className="w-4 h-4" />
                <span>Powered by LangGraph & Gemini</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <Palette className="w-4 h-4" />
                <span>Creative UI Design</span>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Zap className="w-4 h-4 text-yellow-500" />
              <span>Multi-Agent AI System</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;