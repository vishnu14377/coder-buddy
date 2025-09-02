import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Send, 
  Sparkles, 
  Code, 
  Loader2, 
  CheckCircle, 
  AlertCircle,
  Lightbulb,
  Rocket
} from 'lucide-react';

const ProjectGenerator = () => {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const samplePrompts = [
    "Create a modern todo app with React and local storage",
    "Build a colorful weather dashboard with animations",
    "Make a creative portfolio website with gradient backgrounds",
    "Design a vibrant calculator with advanced operations",
    "Create a fun memory card game with animations"
  ];

  const handleGenerate = async () => {
    if (!prompt.trim()) return;

    setIsGenerating(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('/api/generate-project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });

      const data = await response.json();

      if (data.success) {
        setResult(data);
      } else {
        setError(data.detail || 'Failed to generate project');
      }
    } catch (err) {
      setError('Network error: Unable to connect to the server');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleGenerate();
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div 
        className="text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-purple-100 to-blue-100 px-4 py-2 rounded-full mb-4">
          <Rocket className="w-5 h-5 text-purple-600" />
          <span className="text-purple-700 font-medium">Project Generator</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Create Amazing Projects with AI
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Describe your project idea and watch our multi-agent system transform it into working code
        </p>
      </motion.div>

      {/* Input Section */}
      <motion.div
        className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
      >
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              <Lightbulb className="w-4 h-4 inline mr-2 text-yellow-500" />
              Describe your project idea
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="e.g., Create a modern todo app with drag and drop functionality, colorful design, and local storage..."
              className="w-full h-32 px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none transition-all"
              disabled={isGenerating}
            />
          </div>

          <motion.button
            onClick={handleGenerate}
            disabled={!prompt.trim() || isGenerating}
            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white font-medium py-4 px-6 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:from-purple-700 hover:to-blue-700 flex items-center justify-center space-x-2"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {isGenerating ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Generating Project...</span>
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                <span>Generate Project</span>
              </>
            )}
          </motion.button>
        </div>
      </motion.div>

      {/* Sample Prompts */}
      <motion.div
        className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6 border border-blue-100"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <Sparkles className="w-5 h-5 mr-2 text-blue-500" />
          Try These Sample Ideas
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {samplePrompts.map((sample, index) => (
            <motion.button
              key={index}
              onClick={() => setPrompt(sample)}
              className="text-left p-3 bg-white/70 rounded-lg border border-blue-200/50 hover:bg-white hover:border-blue-300 transition-all text-sm text-gray-700"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {sample}
            </motion.button>
          ))}
        </div>
      </motion.div>

      {/* Results */}
      {error && (
        <motion.div
          className="bg-red-50 border border-red-200 rounded-2xl p-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-start space-x-3">
            <AlertCircle className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-lg font-semibold text-red-800 mb-2">Generation Failed</h3>
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        </motion.div>
      )}

      {result && (
        <motion.div
          className="bg-green-50 border border-green-200 rounded-2xl p-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-start space-x-3">
            <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-green-800 mb-2">
                Project Generated Successfully!
              </h3>
              <p className="text-green-700 mb-4">{result.message}</p>
              
              {result.session_info && (
                <div className="bg-white/70 rounded-lg p-4 border border-green-200">
                  <h4 className="font-medium text-green-800 mb-2 flex items-center">
                    <Code className="w-4 h-4 mr-2" />
                    Session Details
                  </h4>
                  <div className="text-sm text-green-700 space-y-1">
                    <p><strong>Session ID:</strong> {result.session_info.session_id}</p>
                    <p><strong>Status:</strong> {result.session_info.status}</p>
                    {result.session_info.steps && (
                      <p><strong>Steps Completed:</strong> {result.session_info.steps.length}</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      )}

      {/* Process Indicator */}
      {isGenerating && (
        <motion.div
          className="bg-blue-50 border border-blue-200 rounded-2xl p-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center space-x-4">
            <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
            <div>
              <h3 className="text-lg font-semibold text-blue-800">Processing Your Request</h3>
              <p className="text-blue-600">Our AI agents are working on your project...</p>
              <div className="flex items-center space-x-4 mt-3 text-sm text-blue-600">
                <span className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                  <span>Planner Agent</span>
                </span>
                <span className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                  <span>Architect Agent</span>
                </span>
                <span className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span>Coder Agent</span>
                </span>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default ProjectGenerator;