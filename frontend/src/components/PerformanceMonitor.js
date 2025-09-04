import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Zap, 
  Clock, 
  TrendingUp, 
  Database, 
  Activity,
  CheckCircle,
  AlertCircle,
  Cpu
} from 'lucide-react';

const PerformanceMonitor = () => {
  const [metrics, setMetrics] = useState({
    responseTime: 0,
    cacheHits: 0,
    optimizationsActive: false,
    lastUpdate: new Date()
  });
  const [recentResponses, setRecentResponses] = useState([]);
  const [isOptimized, setIsOptimized] = useState(true);

  useEffect(() => {
    // Check performance status on mount
    checkPerformanceStatus();
    
    // Set up periodic performance monitoring
    const interval = setInterval(checkPerformanceStatus, 5000);
    
    return () => clearInterval(interval);
  }, []);

  const checkPerformanceStatus = async () => {
    try {
      const start = performance.now();
      const response = await fetch('/api/health');
      const end = performance.now();
      const responseTime = end - start;
      
      if (response.ok) {
        const data = await response.json();
        setMetrics(prev => ({
          ...prev,
          responseTime: responseTime,
          optimizationsActive: data.optimizations_active || false,
          lastUpdate: new Date()
        }));
      }
    } catch (error) {
      console.error('Performance check failed:', error);
    }
  };

  const testQuickResponse = async () => {
    const testQuestions = [
      "What is Python?",
      "What is JavaScript?",
      "What is React?",
      "Difference between Python and JavaScript"
    ];
    
    const randomQuestion = testQuestions[Math.floor(Math.random() * testQuestions.length)];
    
    try {
      const start = performance.now();
      const response = await fetch('/api/ask-question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: randomQuestion, context: "" })
      });
      const end = performance.now();
      const responseTime = end - start;
      
      if (response.ok) {
        const data = await response.json();
        const newResponse = {
          question: randomQuestion,
          responseTime: responseTime,
          cached: data.cached || responseTime < 100,
          timestamp: new Date()
        };
        
        setRecentResponses(prev => [newResponse, ...prev.slice(0, 4)]);
      }
    } catch (error) {
      console.error('Test failed:', error);
    }
  };

  const getPerformanceColor = (time) => {
    if (time < 100) return 'text-green-600';
    if (time < 500) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getPerformanceBadge = (time) => {
    if (time < 50) return { text: 'Ultra Fast ⚡', color: 'bg-green-100 text-green-800' };
    if (time < 200) return { text: 'Fast 🚀', color: 'bg-blue-100 text-blue-800' };
    if (time < 1000) return { text: 'Good 👍', color: 'bg-yellow-100 text-yellow-800' };
    return { text: 'Slow 🐌', color: 'bg-red-100 text-red-800' };
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
          <span className="text-green-700 font-medium">Performance Monitor</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          System Performance ⚡
        </h2>
        <p className="text-gray-600">
          Real-time performance metrics and optimization status
        </p>
      </motion.div>

      {/* Performance Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <motion.div
          className="bg-white rounded-xl p-6 shadow-lg border border-gray-100"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Response Time</p>
              <p className={`text-2xl font-bold ${getPerformanceColor(metrics.responseTime)}`}>
                {metrics.responseTime.toFixed(0)}ms
              </p>
            </div>
            <Clock className={`w-8 h-8 ${getPerformanceColor(metrics.responseTime)}`} />
          </div>
          <div className="mt-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPerformanceBadge(metrics.responseTime).color}`}>
              {getPerformanceBadge(metrics.responseTime).text}
            </span>
          </div>
        </motion.div>

        <motion.div
          className="bg-white rounded-xl p-6 shadow-lg border border-gray-100"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Optimizations</p>
              <p className="text-2xl font-bold text-green-600">
                {isOptimized ? "Active" : "Inactive"}
              </p>
            </div>
            <Zap className={`w-8 h-8 ${isOptimized ? 'text-green-600' : 'text-gray-400'}`} />
          </div>
          <div className="mt-2">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              isOptimized ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
            }`}>
              {isOptimized ? "Fast Mode ⚡" : "Standard Mode"}
            </span>
          </div>
        </motion.div>

        <motion.div
          className="bg-white rounded-xl p-6 shadow-lg border border-gray-100"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">Cache Status</p>
              <p className="text-2xl font-bold text-blue-600">Ready</p>
            </div>
            <Database className="w-8 h-8 text-blue-600" />
          </div>
          <div className="mt-2">
            <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
              Smart Caching 🧠
            </span>
          </div>
        </motion.div>

        <motion.div
          className="bg-white rounded-xl p-6 shadow-lg border border-gray-100"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-500">AI Model</p>
              <p className="text-2xl font-bold text-purple-600">Fast</p>
            </div>
            <Cpu className="w-8 h-8 text-purple-600" />
          </div>
          <div className="mt-2">
            <span className="px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
              Gemini Flash-8B ⚡
            </span>
          </div>
        </motion.div>
      </div>

      {/* Performance Test */}
      <motion.div
        className="bg-white rounded-xl p-6 shadow-lg border border-gray-100"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-800">Performance Test</h3>
          <motion.button
            onClick={testQuickResponse}
            className="bg-gradient-to-r from-green-500 to-blue-600 text-white px-4 py-2 rounded-lg flex items-center space-x-2 hover:from-green-600 hover:to-blue-700 transition-all"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <TrendingUp className="w-4 h-4" />
            <span>Test Speed</span>
          </motion.button>
        </div>
        
        <p className="text-gray-600 mb-4">
          Click "Test Speed" to measure real-time Q&A response performance
        </p>

        {recentResponses.length > 0 && (
          <div className="space-y-2">
            <h4 className="font-medium text-gray-700 mb-2">Recent Test Results:</h4>
            {recentResponses.map((test, index) => (
              <motion.div
                key={index}
                className="flex items-center justify-between bg-gray-50 p-3 rounded-lg"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-800 truncate">
                    {test.question}
                  </p>
                  <p className="text-xs text-gray-500">
                    {test.timestamp.toLocaleTimeString()}
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  {test.cached && (
                    <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                      Cached
                    </span>
                  )}
                  <span className={`font-bold ${getPerformanceColor(test.responseTime)}`}>
                    {test.responseTime.toFixed(0)}ms
                  </span>
                  {test.responseTime < 100 ? (
                    <CheckCircle className="w-4 h-4 text-green-600" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-yellow-600" />
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>

      {/* Optimization Features */}
      <motion.div
        className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <Zap className="w-5 h-5 mr-2 text-blue-600" />
          Active Optimizations
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center space-x-3">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <div>
              <p className="font-medium text-gray-800">Ultra-Fast Models</p>
              <p className="text-sm text-gray-600">Gemini Flash-8B for instant responses</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <div>
              <p className="font-medium text-gray-800">Smart Caching</p>
              <p className="text-sm text-gray-600">Memory + disk cache for common questions</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <div>
              <p className="font-medium text-gray-800">Parallel Processing</p>
              <p className="text-sm text-gray-600">Concurrent file generation</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <div>
              <p className="font-medium text-gray-800">Project Templates</p>
              <p className="text-sm text-gray-600">Pre-built templates for instant projects</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default PerformanceMonitor;