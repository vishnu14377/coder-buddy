import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MessageCircle, 
  Send, 
  Bot, 
  User, 
  Trash2, 
  History,
  Clock,
  Zap,
  CheckCircle
} from 'lucide-react';

const EnhancedQAChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [responseTime, setResponseTime] = useState(0);
  const messagesEndRef = useRef(null);
  const maxMessages = 4; // Keep only 4 messages (2 pairs of Q&A)

  // Load chat history from localStorage on component mount
  useEffect(() => {
    const savedMessages = localStorage.getItem('qa-chat-history');
    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        setMessages(parsed);
      } catch (error) {
        console.error('Error loading chat history:', error);
      }
    }
  }, []);

  // Save chat history to localStorage whenever messages change
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('qa-chat-history', JSON.stringify(messages));
    }
  }, [messages]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Clean up old messages to keep only the most recent ones
  const cleanupMessages = (currentMessages) => {
    if (currentMessages.length > maxMessages) {
      // Keep only the most recent messages
      return currentMessages.slice(-maxMessages);
    }
    return currentMessages;
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    // Add user message and clean up if needed
    let updatedMessages = [...messages, userMessage];
    updatedMessages = cleanupMessages(updatedMessages);
    setMessages(updatedMessages);
    
    const currentInput = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    const startTime = performance.now();

    try {
      const response = await fetch('/api/ask-question', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: currentInput,
          context: ''
        }),
      });

      const endTime = performance.now();
      setResponseTime(endTime - startTime);

      if (response.ok) {
        const data = await response.json();
        
        const botMessage = {
          id: Date.now() + 1,
          type: 'bot',
          content: data.answer,
          timestamp: new Date(),
          responseTime: data.response_time_ms || (endTime - startTime),
          cached: data.cached || false,
          technical: data.is_technical || false
        };

        // Add bot message and clean up if needed
        let newMessages = [...updatedMessages, botMessage];
        newMessages = cleanupMessages(newMessages);
        setMessages(newMessages);
        
      } else {
        throw new Error('Network response was not ok');
      }
    } catch (error) {
      console.error('Error:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
        isError: true
      };

      let newMessages = [...updatedMessages, errorMessage];
      newMessages = cleanupMessages(newMessages);
      setMessages(newMessages);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem('qa-chat-history');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const suggestedQuestions = [
    "What is React?",
    "How to learn JavaScript?",
    "Explain CSS Flexbox",
    "What is Node.js?",
    "Python vs JavaScript differences"
  ];

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Header */}
      <motion.div 
        className="text-center mb-6"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="inline-flex items-center space-x-2 bg-gradient-to-r from-blue-100 to-purple-100 px-4 py-2 rounded-full mb-4">
          <MessageCircle className="w-5 h-5 text-blue-600" />
          <span className="text-blue-700 font-medium">Smart Q&A Assistant</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Ask Anything 🤖
        </h2>
        <p className="text-gray-600">
          Ultra-fast responses with smart caching • Auto-saves last {maxMessages} messages
        </p>
        
        {/* Stats */}
        <div className="flex items-center justify-center space-x-6 mt-4">
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <History className="w-4 h-4" />
            <span>{messages.length} messages</span>
          </div>
          {responseTime > 0 && (
            <div className="flex items-center space-x-2 text-sm text-green-600">
              <Zap className="w-4 h-4" />
              <span>Last: {responseTime.toFixed(0)}ms</span>
            </div>
          )}
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="flex items-center space-x-1 text-sm text-red-600 hover:text-red-700 transition-colors"
            >
              <Trash2 className="w-4 h-4" />
              <span>Clear</span>
            </button>
          )}
        </div>
      </motion.div>

      {/* Chat Messages */}
      <div className="flex-1 bg-white rounded-xl shadow-lg border border-gray-100 flex flex-col overflow-hidden">
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <motion.div 
              className="text-center py-8"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <Bot className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-600 mb-2">
                Start a conversation
              </h3>
              <p className="text-gray-500 mb-6">
                Ask any programming question or try one of these:
              </p>
              
              {/* Suggested Questions */}
              <div className="flex flex-wrap justify-center gap-2">
                {suggestedQuestions.map((question, index) => (
                  <motion.button
                    key={index}
                    onClick={() => setInputMessage(question)}
                    className="px-3 py-2 bg-blue-50 text-blue-700 rounded-full text-sm hover:bg-blue-100 transition-colors"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {question}
                  </motion.button>
                ))}
              </div>
            </motion.div>
          ) : (
            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex space-x-3 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : ''}`}>
                    {/* Avatar */}
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.type === 'user' 
                        ? 'bg-blue-600' 
                        : message.isError 
                          ? 'bg-red-600' 
                          : 'bg-gray-600'
                    }`}>
                      {message.type === 'user' 
                        ? <User className="w-4 h-4 text-white" />
                        : <Bot className="w-4 h-4 text-white" />
                      }
                    </div>
                    
                    {/* Message Bubble */}
                    <div className={`rounded-2xl px-4 py-3 ${
                      message.type === 'user'
                        ? 'bg-blue-600 text-white'
                        : message.isError
                          ? 'bg-red-50 border border-red-200 text-red-800'
                          : 'bg-gray-50 border border-gray-200 text-gray-800'
                    }`}>
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">
                        {message.content}
                      </div>
                      
                      {/* Message metadata */}
                      <div className={`flex items-center justify-between mt-2 text-xs ${
                        message.type === 'user' ? 'text-blue-200' : 'text-gray-500'
                      }`}>
                        <div className="flex items-center space-x-2">
                          <Clock className="w-3 h-3" />
                          <span>{formatTime(message.timestamp)}</span>
                          
                          {message.type === 'bot' && message.responseTime && (
                            <>
                              <span>•</span>
                              <div className="flex items-center space-x-1">
                                <Zap className="w-3 h-3" />
                                <span>{message.responseTime.toFixed(0)}ms</span>
                              </div>
                            </>
                          )}
                          
                          {message.cached && (
                            <>
                              <span>•</span>
                              <div className="flex items-center space-x-1">
                                <CheckCircle className="w-3 h-3" />
                                <span>Cached</span>
                              </div>
                            </>
                          )}
                          
                          {message.technical && (
                            <>
                              <span>•</span>
                              <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded text-xs">
                                Technical
                              </span>
                            </>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          )}
          
          {/* Loading indicator */}
          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="flex space-x-3">
                <div className="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center">
                  <Bot className="w-4 h-4 text-white" />
                </div>
                <div className="bg-gray-50 border border-gray-200 rounded-2xl px-4 py-3">
                  <div className="flex space-x-1">
                    <motion.div
                      className="w-2 h-2 bg-gray-400 rounded-full"
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                    />
                    <motion.div
                      className="w-2 h-2 bg-gray-400 rounded-full"
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
                    />
                    <motion.div
                      className="w-2 h-2 bg-gray-400 rounded-full"
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
                    />
                  </div>
                </div>
              </div>
            </motion.div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-100 p-4">
          <div className="flex space-x-3">
            <div className="flex-1 relative">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask any programming question..."
                className="w-full px-4 py-3 border border-gray-300 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="1"
                style={{ minHeight: '50px', maxHeight: '120px' }}
                disabled={isLoading}
              />
              
              {/* Character/Message counter */}
              <div className="absolute bottom-2 right-2 text-xs text-gray-400">
                {messages.length}/{maxMessages} messages
              </div>
            </div>
            
            <motion.button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className={`px-6 py-3 rounded-xl font-medium transition-all ${
                inputMessage.trim() && !isLoading
                  ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg hover:shadow-xl'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
              }`}
              whileHover={inputMessage.trim() ? { scale: 1.05 } : {}}
              whileTap={inputMessage.trim() ? { scale: 0.95 } : {}}
            >
              <Send className="w-5 h-5" />
            </motion.button>
          </div>
          
          {/* Message limit warning */}
          {messages.length >= maxMessages - 1 && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-2 text-xs text-amber-600 bg-amber-50 px-3 py-2 rounded-lg"
            >
              ⚠️ Only {maxMessages} messages are kept. Older messages will be automatically deleted.
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EnhancedQAChat;