"""
Ultra-fast Q&A Agent with caching, optimized models, and parallel processing.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict, Any, Optional
import os
import asyncio
import time
import hashlib
import pickle
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

class FastCache:
    """In-memory cache with disk persistence for ultra-fast responses."""
    
    def __init__(self, cache_dir: str = "/tmp/coder_buddy_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache = {}
        self.max_memory_size = 1000  # Max items in memory cache
        
    def _get_key_hash(self, key: str) -> str:
        """Generate a hash for the cache key."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[str]:
        """Get cached response."""
        key_hash = self._get_key_hash(key)
        
        # Check memory cache first
        if key_hash in self.memory_cache:
            return self.memory_cache[key_hash]
        
        # Check disk cache
        cache_file = self.cache_dir / f"{key_hash}.pkl"
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    data = pickle.load(f)
                    # Add to memory cache
                    if len(self.memory_cache) < self.max_memory_size:
                        self.memory_cache[key_hash] = data
                    return data
            except:
                pass
        
        return None
    
    def set(self, key: str, value: str):
        """Set cached response."""
        key_hash = self._get_key_hash(key)
        
        # Save to memory cache
        if len(self.memory_cache) < self.max_memory_size:
            self.memory_cache[key_hash] = value
        
        # Save to disk cache
        cache_file = self.cache_dir / f"{key_hash}.pkl"
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(value, f)
        except:
            pass

class UltraFastQAAgent:
    """Ultra-fast Q&A agent with multiple optimizations."""
    
    def __init__(self):
        # Use the fastest Gemini model
        self.fast_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-8b",  # Fastest model
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1,  # Lower temperature for faster responses
            max_tokens=500,   # Limit tokens for faster responses
            request_timeout=5  # 5 second timeout
        )
        
        # Fallback to standard model for complex queries
        self.standard_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3,
            request_timeout=10
        )
        
        self.cache = FastCache()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Pre-compiled system prompts for speed
        self.system_prompts = {
            'technical': """You are a fast technical assistant. Provide concise, accurate code examples and explanations. Keep responses under 400 words unless specifically asked for more detail.""",
            'general': """You are a helpful assistant. Provide clear, concise answers. Keep responses under 300 words unless specifically asked for more detail.""",
            'quick': """Provide a brief, direct answer in 1-2 sentences."""
        }
        
        # Common question patterns for ultra-fast responses
        self.quick_responses = {
            'what is python': "Python is a high-level, interpreted programming language known for its simplicity and readability. It's widely used for web development, data science, AI, and automation.",
            'what is javascript': "JavaScript is a programming language primarily used for web development to create interactive web pages and applications. It runs in browsers and on servers (Node.js).",
            'what is react': "React is a popular JavaScript library for building user interfaces, especially web applications. It uses components and virtual DOM for efficient rendering.",
            'difference between python and javascript': "Python is server-side focused with simple syntax, while JavaScript is primarily for web development. Python uses indentation; JavaScript uses brackets.",
            'what is html': "HTML (HyperText Markup Language) is the standard markup language for creating web pages. It uses tags to structure content like headings, paragraphs, and links.",
            'what is css': "CSS (Cascading Style Sheets) is a language used to style and layout web pages created with HTML. It controls colors, fonts, spacing, and responsive design."
        }
    
    def _normalize_question(self, question: str) -> str:
        """Normalize question for cache lookup."""
        return question.lower().strip().replace('?', '').replace('.', '').replace(',', '')
    
    def _get_prompt_type(self, question: str) -> str:
        """Determine the best prompt type for the question."""
        question_lower = question.lower()
        
        # Technical keywords
        technical_keywords = [
            'code', 'programming', 'python', 'javascript', 'react', 'api',
            'database', 'sql', 'html', 'css', 'debug', 'error', 'function',
            'algorithm', 'framework', 'library'
        ]
        
        # Quick answer keywords
        quick_keywords = ['what is', 'define', 'meaning of', 'difference between']
        
        if any(keyword in question_lower for keyword in quick_keywords):
            return 'quick'
        elif any(keyword in question_lower for keyword in technical_keywords):
            return 'technical'
        else:
            return 'general'
    
    def _is_simple_question(self, question: str) -> bool:
        """Check if question can be answered with predefined responses."""
        normalized = self._normalize_question(question)
        return normalized in self.quick_responses
    
    async def answer_question_async(self, question: str, context: str = "") -> str:
        """Async version for even faster responses."""
        start_time = time.time()
        
        # Check for ultra-fast predefined responses
        normalized_question = self._normalize_question(question)
        if normalized_question in self.quick_responses:
            response = self.quick_responses[normalized_question]
            print(f"⚡ Ultra-fast response in {(time.time() - start_time)*1000:.1f}ms")
            return response
        
        # Check cache
        cache_key = f"{question}|{context}"
        cached_response = self.cache.get(cache_key)
        if cached_response:
            print(f"🚀 Cached response in {(time.time() - start_time)*1000:.1f}ms")
            return cached_response
        
        # Determine optimal prompt and model
        prompt_type = self._get_prompt_type(question)
        
        # Use fast model for simple questions
        llm = self.fast_llm if prompt_type in ['quick', 'general'] else self.standard_llm
        system_prompt = self.system_prompts[prompt_type]
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
Question: {question}
{f"Context: {context}" if context else ""}

Provide a helpful, concise answer.
""")
        ]
        
        try:
            # Run in executor for true async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self.executor, 
                lambda: llm.invoke(messages)
            )
            
            answer = response.content
            
            # Cache the response
            self.cache.set(cache_key, answer)
            
            elapsed = (time.time() - start_time) * 1000
            print(f"🔥 Generated response in {elapsed:.1f}ms")
            return answer
            
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            print(f"❌ Error after {elapsed:.1f}ms: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def answer_question(self, question: str, context: str = "") -> str:
        """Synchronous wrapper for compatibility."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self.answer_question_async(question, context))
        except RuntimeError:
            # If event loop is already running, use sync approach
            return self._answer_question_sync(question, context)
    
    def _answer_question_sync(self, question: str, context: str = "") -> str:
        """Optimized synchronous version."""
        start_time = time.time()
        
        # Check for ultra-fast predefined responses
        normalized_question = self._normalize_question(question)
        if normalized_question in self.quick_responses:
            response = self.quick_responses[normalized_question]
            print(f"⚡ Ultra-fast response in {(time.time() - start_time)*1000:.1f}ms")
            return response
        
        # Check cache
        cache_key = f"{question}|{context}"
        cached_response = self.cache.get(cache_key)
        if cached_response:
            print(f"🚀 Cached response in {(time.time() - start_time)*1000:.1f}ms")
            return cached_response
        
        # Determine optimal prompt and model
        prompt_type = self._get_prompt_type(question)
        llm = self.fast_llm if prompt_type in ['quick', 'general'] else self.standard_llm
        system_prompt = self.system_prompts[prompt_type]
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"""
Question: {question}
{f"Context: {context}" if context else ""}

Provide a helpful, concise answer.
""")
        ]
        
        try:
            response = llm.invoke(messages)
            answer = response.content
            
            # Cache the response
            self.cache.set(cache_key, answer)
            
            elapsed = (time.time() - start_time) * 1000
            print(f"🔥 Generated response in {elapsed:.1f}ms")
            return answer
            
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            print(f"❌ Error after {elapsed:.1f}ms: {str(e)}")            
            return f"Sorry, I encountered an error: {str(e)}"
    
    def is_technical_question(self, question: str) -> bool:
        """Fast technical question detection."""
        return self._get_prompt_type(question) == 'technical'
    
    def warm_up_cache(self):
        """Pre-populate cache with common responses."""
        common_questions = [
            "What is Python?",
            "What is JavaScript?", 
            "What is React?",
            "What is HTML?",
            "What is CSS?",
            "Difference between Python and JavaScript",
            "How to learn programming?",
            "What is an API?",
            "What is a database?",
            "What is Git?"
        ]
        
        print("🔥 Warming up cache with common questions...")
        for question in common_questions:
            try:
                self.answer_question(question)
            except:
                pass
        print("✅ Cache warmed up!")

# Create global ultra-fast instance
ultra_fast_qa_agent = UltraFastQAAgent()

# Warm up cache on import (disabled to avoid quota issues during startup)
# ultra_fast_qa_agent.warm_up_cache()