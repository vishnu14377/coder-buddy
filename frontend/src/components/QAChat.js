import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Send, 
  MessageCircle, 
  Bot, 
  User, 
  Loader2, 
  Brain,
  Code,
  HelpCircle,
  Sparkles
} from 'lucide-react';

const QAChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: "👋 Hi! I'm your AI assistant. I can help with both technical programming questions and general knowledge. What would you like to know?",
      timestamp: new Date().toISOString(),
      isTyping: false
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const sampleQuestions = [
    { text: "How do I implement authentication in React?", type: "technical", icon: Code },
    { text: "What's the difference between Python and JavaScript?", type: "technical", icon: Code },
    { text: "Explain machine learning in simple terms", type: "general", icon: Brain },
    { text: "How does blockchain technology work?", type: "general", icon: HelpCircle }
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Add typing indicator
    const typingMessage = {
      id: Date.now() + 1,
      type: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
      isTyping: true
    };
    setMessages(prev => [...prev, typingMessage]);

    try {
      const response = await fetch('/api/ask-question', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          question: userMessage.content,
          context: '' 
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        throw new Error(`Expected JSON response, got: ${text.substring(0, 100)}...`);
      }

      const data = await response.json();

      if (data.success) {
        const assistantMessage = {
          id: Date.now() + 2,
          type: 'assistant',
          content: data.answer,
          timestamp: new Date().toISOString(),
          isTechnical: data.is_technical,
          isTyping: false
        };

        // Remove typing indicator and add real message
        setMessages(prev => prev.slice(0, -1).concat(assistantMessage));
      } else {
        throw new Error(data.detail || 'Failed to get response');
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 3,
        type: 'assistant',
        content: `Sorry, I encountered an error: ${error.message}`,
        timestamp: new Date().toISOString(),
        isError: true,
        isTyping: false
      };
      
      // Remove typing indicator and add error message
      setMessages(prev => prev.slice(0, -1).concat(errorMessage));
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSampleQuestion = (question) => {
    setInputValue(question);
    textareaRef.current?.focus();
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <motion.div 
        className="text-center"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 rounded-full mb-4">
          <MessageCircle className="w-5 h-5 text-blue-600" />
          <span className="text-blue-700 font-medium">Q&A Assistant</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Ask Me Anything
        </h2>
        <p className="text-gray-600">
          Technical programming help or general knowledge - I'm here to assist!
        </p>
      </motion.div>

      {/* Sample Questions */}
      <motion.div
        className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl p-6 border border-indigo-100"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
          <Sparkles className="w-5 h-5 mr-2 text-indigo-500" />
          Try These Questions
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {sampleQuestions.map((sample, index) => {
            const Icon = sample.icon;
            return (
              <motion.button
                key={index}
                onClick={() => handleSampleQuestion(sample.text)}
                className="text-left p-3 bg-white/70 rounded-lg border border-indigo-200/50 hover:bg-white hover:border-indigo-300 transition-all text-sm text-gray-700 flex items-start space-x-2"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Icon className={`w-4 h-4 mt-0.5 flex-shrink-0 ${
                  sample.type === 'technical' ? 'text-blue-500' : 'text-purple-500'
                }`} />
                <span>{sample.text}</span>
              </motion.button>
            );
          })}
        </div>
      </motion.div>

      {/* Chat Container */}
      <motion.div
        className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
      >
        {/* Messages */}
        <div className="h-96 overflow-y-auto p-6 space-y-4 chat-container">
          {messages.map((message) => (
            <motion.div
              key={message.id}
              className={`flex items-start space-x-3 ${
                message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
              }`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                message.type === 'user' 
                  ? 'bg-gradient-to-r from-blue-500 to-purple-500' 
                  : 'bg-gradient-to-r from-green-400 to-blue-500'
              }`}>
                {message.type === 'user' ? (
                  <User className="w-4 h-4 text-white" />
                ) : (
                  <Bot className="w-4 h-4 text-white" />
                )}
              </div>
              
              <div className={`flex-1 ${message.type === 'user' ? 'text-right' : ''}`}>
                <div className={`inline-block max-w-3xl rounded-2xl px-4 py-3 ${
                  message.type === 'user'
                    ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                    : message.isError
                    ? 'bg-red-50 text-red-800 border border-red-200'
                    : 'bg-gray-50 text-gray-800'
                }`}>
                  {message.isTyping ? (
                    <div className="flex items-center space-x-2">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span className="text-sm">Thinking...</span>
                    </div>
                  ) : (
                    <div>
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      {message.isTechnical && (
                        <div className="mt-2 text-xs opacity-75 flex items-center space-x-1">
                          <Code className="w-3 h-3" />
                          <span>Technical Question</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>
                <div className={`text-xs text-gray-500 mt-1 ${
                  message.type === 'user' ? 'text-right' : 'text-left'
                }`}>
                  {formatTimestamp(message.timestamp)}
                </div>
              </div>
            </motion.div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-100 p-4">
          <div className="flex items-end space-x-3">
            <div className="flex-1">
              <textarea
                ref={textareaRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything... (Press Enter to send)"
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-all"
                rows="2"
                disabled={isLoading}
              />
            </div>
            <motion.button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="bg-gradient-to-r from-blue-500 to-purple-500 text-white p-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all hover:from-blue-600 hover:to-purple-600"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </motion.button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default QAChat;