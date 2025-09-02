"""
General Q&A Agent for handling both technical and general knowledge questions.
"""

from langchain_groq.chat_models import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class GeneralQAAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY")
        )
        
    def get_system_prompt(self) -> str:
        return """You are a comprehensive AI assistant capable of helping with both technical programming questions and general knowledge inquiries.

For TECHNICAL questions:
- Provide detailed code examples and explanations
- Suggest best practices and modern approaches
- Help debug issues and optimize solutions
- Cover multiple programming languages and frameworks

For GENERAL questions:
- Provide accurate, helpful information on a wide range of topics
- Be conversational and engaging
- Cite sources when appropriate
- Admit when you're uncertain about something

Always:
- Be friendly and approachable
- Provide clear, well-structured responses
- Ask clarifying questions when needed
- Offer practical, actionable advice
"""

    def answer_question(self, question: str, context: str = "") -> str:
        """
        Answer a general or technical question.
        
        Args:
            question: The user's question
            context: Additional context if available
            
        Returns:
            The AI's response
        """
        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=f"""
Question: {question}

{f"Additional Context: {context}" if context else ""}

Please provide a helpful, comprehensive answer.
""")
        ]
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Sorry, I encountered an error while processing your question: {str(e)}"

    def is_technical_question(self, question: str) -> bool:
        """
        Determine if a question is technical/programming related.
        """
        technical_keywords = [
            'code', 'programming', 'python', 'javascript', 'react', 'api',
            'database', 'sql', 'html', 'css', 'debug', 'error', 'function',
            'variable', 'algorithm', 'data structure', 'framework', 'library',
            'git', 'github', 'deployment', 'server', 'backend', 'frontend'
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in technical_keywords)

# Global instance for easy access
qa_agent = GeneralQAAgent()