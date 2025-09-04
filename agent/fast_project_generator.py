"""
Ultra-fast project generator with parallel processing and optimized workflows.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any, List
import os
import asyncio
import time
import json
import re
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from agent.states import Plan, File, TaskPlan, ImplementationTask, CoderState
from agent.tools import write_file, read_file
from agent.monitoring import workflow_monitor

load_dotenv()

class FastProjectGenerator:
    """Ultra-fast project generator with parallel processing."""
    
    def __init__(self):
        # Use fastest model for simple tasks
        self.fast_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-8b",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1,
            max_tokens=1000,
            request_timeout=8
        )
        
        # Standard model for complex tasks
        self.standard_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3,
            request_timeout=15
        )
        
        self.executor = ThreadPoolExecutor(max_workers=6)
        
        # Pre-compiled templates for common project types
        self.project_templates = {
            'todo_app': {
                'name': 'Modern Todo App',
                'description': 'A sleek todo application with local storage',
                'techstack': 'HTML, CSS, JavaScript',
                'features': ['Add tasks', 'Mark complete', 'Delete tasks', 'Local storage', 'Responsive design'],
                'files': [
                    {'path': 'index.html', 'purpose': 'Main HTML structure'},
                    {'path': 'style.css', 'purpose': 'Styling and layout'},
                    {'path': 'script.js', 'purpose': 'JavaScript functionality'}
                ]
            },
            'calculator': {
                'name': 'Modern Calculator',
                'description': 'A colorful calculator with advanced operations',
                'techstack': 'HTML, CSS, JavaScript',
                'features': ['Basic math operations', 'Colorful design', 'Keyboard support', 'History display'],
                'files': [
                    {'path': 'index.html', 'purpose': 'Calculator interface'},
                    {'path': 'style.css', 'purpose': 'Modern styling'},
                    {'path': 'script.js', 'purpose': 'Calculator logic'}
                ]
            },
            'portfolio': {
                'name': 'Creative Portfolio',
                'description': 'A personal portfolio website with modern design',
                'techstack': 'HTML, CSS, JavaScript',
                'features': ['Hero section', 'Projects showcase', 'About section', 'Contact form', 'Animations'],
                'files': [
                    {'path': 'index.html', 'purpose': 'Main portfolio structure'},
                    {'path': 'style.css', 'purpose': 'Creative styling and animations'},
                    {'path': 'script.js', 'purpose': 'Interactive features'}
                ]
            }
        }
        
        # Pre-compiled code templates
        self.code_templates = {
            'html_base': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    {body_content}
    <script src="script.js"></script>
</body>
</html>''',
            'css_modern': '''/* Modern CSS Reset and Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        padding: 15px;
    }
}'''
        }
    
    def _detect_project_type(self, prompt: str) -> str:
        """Quickly detect project type from prompt."""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['todo', 'task', 'list']):
            return 'todo_app'
        elif any(word in prompt_lower for word in ['calculator', 'calc', 'math']):
            return 'calculator'
        elif any(word in prompt_lower for word in ['portfolio', 'personal', 'showcase']):
            return 'portfolio'
        else:
            return 'custom'
    
    async def fast_planner_agent(self, user_prompt: str, session_id: str) -> Plan:
        """Ultra-fast planner using templates and parallel processing."""
        start_time = time.time()
        
        workflow_monitor.start_session(session_id, user_prompt)
        workflow_monitor.start_step("Fast Planner", "Analyzing request with templates")
        
        try:
            project_type = self._detect_project_type(user_prompt)
            
            if project_type in self.project_templates:
                # Use pre-compiled template for instant response
                template = self.project_templates[project_type]
                
                files = [File(path=f["path"], purpose=f["purpose"]) for f in template["files"]]
                plan = Plan(
                    name=template["name"],
                    description=template["description"],
                    techstack=template["techstack"],
                    features=template["features"],
                    files=files
                )
                
                elapsed = (time.time() - start_time) * 1000
                print(f"⚡ Template-based plan in {elapsed:.1f}ms")
                
            else:
                # Use fast LLM for custom projects
                prompt_text = f"""Create a project plan for: {user_prompt}

Respond with ONLY a JSON object:
{{
  "name": "Project Name",
  "description": "Brief description", 
  "techstack": "Technologies to use",
  "features": ["feature1", "feature2", "feature3"],
  "files": [
    {{"path": "index.html", "purpose": "Main structure"}},
    {{"path": "style.css", "purpose": "Styling"}},
    {{"path": "script.js", "purpose": "Functionality"}}
  ]
}}"""
                
                response = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    lambda: self.fast_llm.invoke(prompt_text)
                )
                
                # Quick JSON parsing
                content = response.content
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group())
                    files = [File(path=f["path"], purpose=f["purpose"]) for f in data["files"]]
                    plan = Plan(
                        name=data["name"],
                        description=data["description"],
                        techstack=data["techstack"],
                        features=data["features"],
                        files=files
                    )
                else:
                    raise ValueError("Could not parse response")
                
                elapsed = (time.time() - start_time) * 1000
                print(f"🔥 Custom plan in {elapsed:.1f}ms")
            
            workflow_monitor.complete_step(plan.model_dump())
            return plan
            
        except Exception as e:
            workflow_monitor.error_step(str(e))
            raise e
    
    async def fast_architect_agent(self, plan: Plan) -> TaskPlan:
        """Fast architect with parallel task creation."""
        start_time = time.time()
        
        workflow_monitor.start_step("Fast Architect", "Creating implementation tasks")
        
        try:
            # Create tasks in parallel for each file
            async def create_task_for_file(file: File) -> ImplementationTask:
                if file.path.endswith('.html'):
                    task_desc = f"Create {file.path} with modern HTML structure, semantic elements, and proper meta tags."
                elif file.path.endswith('.css'):
                    task_desc = f"Create {file.path} with modern CSS, responsive design, and attractive styling."
                elif file.path.endswith('.js'):
                    task_desc = f"Create {file.path} with clean JavaScript, proper event handling, and modern ES6+ features."
                else:
                    task_desc = f"Create {file.path} implementing {file.purpose}"
                
                return ImplementationTask(filepath=file.path, task_description=task_desc)
            
            # Execute in parallel
            tasks = await asyncio.gather(*[create_task_for_file(file) for file in plan.files])
            
            task_plan = TaskPlan(implementation_steps=tasks)
            task_plan.plan = plan
            
            elapsed = (time.time() - start_time) * 1000
            print(f"⚡ Architecture in {elapsed:.1f}ms")
            
            workflow_monitor.complete_step(task_plan.model_dump())
            return task_plan
            
        except Exception as e:
            workflow_monitor.error_step(str(e))
            raise e
    
    async def fast_coder_agent(self, task_plan: TaskPlan) -> dict:
        """Ultra-fast coder with parallel file generation."""
        start_time = time.time()
        
        workflow_monitor.start_step("Fast Coder", "Generating files in parallel")
        
        try:
            async def generate_file(task: ImplementationTask) -> tuple:
                file_start = time.time()
                
                try:
                    # Use templates for common files
                    if task.filepath == 'index.html':
                        content = await self._generate_html_fast(task_plan.plan)
                    elif task.filepath == 'style.css':
                        content = await self._generate_css_fast(task_plan.plan)
                    elif task.filepath == 'script.js':
                        content = await self._generate_js_fast(task_plan.plan)
                    else:
                        content = await self._generate_custom_file(task)
                    
                    # Write file
                    write_file.run(task.filepath, content)
                    
                    file_elapsed = (time.time() - file_start) * 1000
                    print(f"✅ Generated {task.filepath} in {file_elapsed:.1f}ms")
                    
                    return (task.filepath, "success", content[:100] + "...")
                    
                except Exception as e:
                    file_elapsed = (time.time() - file_start) * 1000
                    print(f"❌ Failed {task.filepath} in {file_elapsed:.1f}ms: {str(e)}")
                    return (task.filepath, "error", str(e))
            
            # Generate all files in parallel
            results = await asyncio.gather(*[generate_file(task) for task in task_plan.implementation_steps])
            
            elapsed = (time.time() - start_time) * 1000
            print(f"🚀 All files generated in {elapsed:.1f}ms")
            
            workflow_monitor.complete_step({"files_generated": len(results), "results": results})
            workflow_monitor.complete_session("Project completed successfully")
            
            return {"status": "DONE", "results": results, "generation_time": elapsed}
            
        except Exception as e:
            workflow_monitor.error_step(str(e))
            return {"status": "ERROR", "error": str(e)}
    
    async def _generate_html_fast(self, plan: Plan) -> str:
        """Generate HTML using templates and fast LLM."""
        project_type = plan.name.lower()
        
        if 'todo' in project_type:
            body_content = '''
    <div class="container">
        <h1>Todo App</h1>
        <div class="input-section">
            <input type="text" id="todoInput" placeholder="Add a new task...">
            <button id="addBtn">Add Task</button>
        </div>
        <ul id="todoList"></ul>
    </div>'''
        elif 'calculator' in project_type:
            body_content = '''
    <div class="calculator">
        <div class="display">
            <input type="text" id="result" readonly>
        </div>
        <div class="buttons">
            <button onclick="clearDisplay()">C</button>
            <button onclick="deleteLast()">⌫</button>
            <button onclick="appendToDisplay('/')">/</button>
            <button onclick="appendToDisplay('*')">×</button>
            <!-- More calculator buttons -->
        </div>
    </div>'''
        else:
            # Use fast LLM for custom HTML
            prompt = f"Generate HTML body content for: {plan.description}. Features: {', '.join(plan.features)}. Keep it clean and semantic."
            response = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: self.fast_llm.invoke(prompt)
            )
            body_content = response.content
        
        return self.code_templates['html_base'].format(
            title=plan.name,
            body_content=body_content
        )
    
    async def _generate_css_fast(self, plan: Plan) -> str:
        """Generate CSS using templates and fast styling."""
        base_css = self.code_templates['css_modern']
        
        # Add specific styles based on project type
        project_type = plan.name.lower()
        
        if 'todo' in project_type:
            specific_css = '''

/* Todo App Styles */
.input-section {
    display: flex;
    gap: 10px;
    margin: 20px 0;
}

#todoInput {
    flex: 1;
    padding: 12px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 16px;
}

#addBtn {
    padding: 12px 24px;
    background: linear-gradient(45deg, #4CAF50, #45a049);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
}

#todoList {
    list-style: none;
}

.todo-item {
    background: white;
    margin: 10px 0;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}'''
        elif 'calculator' in project_type:
            specific_css = '''

/* Calculator Styles */
.calculator {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    max-width: 300px;
    margin: 50px auto;
}

.display input {
    width: 100%;
    height: 60px;
    font-size: 24px;
    text-align: right;
    border: none;
    background: #f1f1f1;
    border-radius: 8px;
    padding: 0 15px;
}

.buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 15px;
}

.buttons button {
    height: 50px;
    font-size: 18px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}'''
        else:
            specific_css = '''

/* Custom Project Styles */
.hero {
    text-align: center;
    padding: 60px 0;
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    margin: 20px 0;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 20px;
    color: white;
}

.btn {
    display: inline-block;
    padding: 12px 30px;
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    text-decoration: none;
    border-radius: 25px;
    transition: transform 0.3s;
}

.btn:hover {
    transform: translateY(-2px);
}'''
        
        return base_css + specific_css
    
    async def _generate_js_fast(self, plan: Plan) -> str:
        """Generate JavaScript using templates and patterns."""
        project_type = plan.name.lower()
        
        if 'todo' in project_type:
            return '''
// Todo App JavaScript
let todos = JSON.parse(localStorage.getItem('todos')) || [];

function renderTodos() {
    const todoList = document.getElementById('todoList');
    todoList.innerHTML = '';
    
    todos.forEach((todo, index) => {
        const li = document.createElement('li');
        li.className = 'todo-item';
        li.innerHTML = `
            <span style="${todo.completed ? 'text-decoration: line-through;' : ''}">${todo.text}</span>
            <div>
                <button onclick="toggleTodo(${index})">${todo.completed ? 'Undo' : 'Done'}</button>
                <button onclick="deleteTodo(${index})">Delete</button>
            </div>
        `;
        todoList.appendChild(li);
    });
}

function addTodo() {
    const input = document.getElementById('todoInput');
    const text = input.value.trim();
    
    if (text) {
        todos.push({ text, completed: false });
        input.value = '';
        saveTodos();
        renderTodos();
    }
}

function toggleTodo(index) {
    todos[index].completed = !todos[index].completed;
    saveTodos();
    renderTodos();
}

function deleteTodo(index) {
    todos.splice(index, 1);
    saveTodos();
    renderTodos();
}

function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

// Event listeners
document.getElementById('addBtn').addEventListener('click', addTodo);
document.getElementById('todoInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTodo();
});

// Initial render
renderTodos();
'''
        elif 'calculator' in project_type:
            return '''
// Calculator JavaScript
let display = document.getElementById('result');
let currentInput = '0';
let shouldResetDisplay = false;

function updateDisplay() {
    display.value = currentInput;
}

function clearDisplay() {
    currentInput = '0';
    updateDisplay();
}

function deleteLast() {
    if (currentInput.length > 1) {
        currentInput = currentInput.slice(0, -1);
    } else {
        currentInput = '0';
    }
    updateDisplay();
}

function appendToDisplay(value) {
    if (shouldResetDisplay) {
        currentInput = '0';
        shouldResetDisplay = false;
    }
    
    if (currentInput === '0' && value !== '.') {
        currentInput = value;
    } else {
        currentInput += value;
    }
    updateDisplay();
}

function calculate() {
    try {
        // Replace × with * for evaluation
        const expression = currentInput.replace(/×/g, '*');
        const result = eval(expression);
        currentInput = result.toString();
        shouldResetDisplay = true;
        updateDisplay();
    } catch (error) {
        currentInput = 'Error';
        shouldResetDisplay = true;
        updateDisplay();
    }
}

// Keyboard support
document.addEventListener('keydown', (e) => {
    if (e.key >= '0' && e.key <= '9' || e.key === '.') {
        appendToDisplay(e.key);
    } else if (e.key === '+' || e.key === '-' || e.key === '*' || e.key === '/') {
        appendToDisplay(e.key);
    } else if (e.key === 'Enter' || e.key === '=') {
        calculate();
    } else if (e.key === 'Escape') {
        clearDisplay();
    } else if (e.key === 'Backspace') {
        deleteLast();
    }
});

updateDisplay();
'''
        else:
            # Generate custom JavaScript with fast LLM
            prompt = f"Generate JavaScript for: {plan.description}. Features: {', '.join(plan.features)}. Use modern ES6+, event listeners, and proper structure."
            response = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                lambda: self.fast_llm.invoke(prompt)
            )
            return response.content
    
    async def _generate_custom_file(self, task: ImplementationTask) -> str:
        """Generate custom file content using fast LLM."""
        prompt = f"Generate content for {task.filepath}: {task.task_description}. Provide clean, modern code."
        response = await asyncio.get_event_loop().run_in_executor(
            self.executor,
            lambda: self.fast_llm.invoke(prompt)
        )
        return response.content
    
    async def generate_project_fast(self, user_prompt: str) -> dict:
        """Main fast project generation method."""
        session_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            print(f"🚀 Starting ultra-fast project generation...")
            
            # Run all agents in optimized sequence
            plan = await self.fast_planner_agent(user_prompt, session_id)
            task_plan = await self.fast_architect_agent(plan)
            result = await self.fast_coder_agent(task_plan)
            
            total_time = (time.time() - start_time) * 1000
            print(f"🎉 Project completed in {total_time:.1f}ms")
            
            return {
                "success": True,
                "session_id": session_id,
                "generation_time": total_time,
                "result": result,
                "message": f"Project generated in {total_time:.0f}ms!"
            }
            
        except Exception as e:
            error_time = (time.time() - start_time) * 1000
            print(f"❌ Error after {error_time:.1f}ms: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "generation_time": error_time
            }

# Global fast generator instance
fast_project_generator = FastProjectGenerator()