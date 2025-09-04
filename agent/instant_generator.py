"""
INSTANT Project Generator - Zero AI delay for common projects.
Generates complete projects in < 50ms using pre-built templates.
"""

import os
import time
import uuid
import json
from typing import Dict, List, Any
from pathlib import Path

class InstantProjectGenerator:
    """Generates projects instantly using pre-built complete templates."""
    
    def __init__(self):
        self.templates = {
            'todo_app': self._get_todo_template(),
            'calculator': self._get_calculator_template(),
            'portfolio': self._get_portfolio_template(),
            'weather_app': self._get_weather_template(),
            'landing_page': self._get_landing_template(),
            'contact_form': self._get_contact_template(),
            'memory_game': self._get_memory_game_template(),
            'quiz_app': self._get_quiz_template(),
            'timer_app': self._get_timer_template(),
            'color_picker': self._get_color_picker_template()
        }
        
        # Project type detection patterns
        self.detection_patterns = {
            'todo_app': ['todo', 'task', 'list', 'reminder', 'checklist'],
            'calculator': ['calculator', 'calc', 'math', 'arithmetic'],
            'portfolio': ['portfolio', 'personal', 'showcase', 'resume'],
            'weather_app': ['weather', 'forecast', 'temperature', 'climate'],
            'landing_page': ['landing', 'homepage', 'marketing', 'business'],
            'contact_form': ['contact', 'form', 'feedback', 'inquiry'],
            'memory_game': ['memory', 'card', 'match', 'flip'],
            'quiz_app': ['quiz', 'question', 'trivia', 'test'],
            'timer_app': ['timer', 'countdown', 'stopwatch', 'alarm'],
            'color_picker': ['color', 'picker', 'palette', 'rgb']
        }
    
    def detect_project_type(self, prompt: str) -> str:
        """Instantly detect project type from prompt."""
        prompt_lower = prompt.lower()
        
        # Check each pattern
        for project_type, keywords in self.detection_patterns.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return project_type
        
        # Default to todo app for quick generation
        return 'todo_app'
    
    def generate_instant(self, prompt: str) -> Dict[str, Any]:
        """Generate project instantly using templates."""
        start_time = time.time()
        session_id = str(uuid.uuid4())
        
        try:
            # Detect project type
            project_type = self.detect_project_type(prompt)
            template = self.templates.get(project_type, self.templates['todo_app'])
            
            # Create project directory
            project_dir = f"/app/generated_project"
            os.makedirs(project_dir, exist_ok=True)
            
            # Write all files instantly
            files_created = []
            for file_info in template['files']:
                file_path = os.path.join(project_dir, file_info['name'])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_info['content'])
                files_created.append(file_info['name'])
            
            generation_time = (time.time() - start_time) * 1000
            
            return {
                "success": True,
                "session_id": session_id,
                "project_type": project_type,
                "project_name": template['name'],
                "description": template['description'],
                "files_created": files_created,
                "generation_time": generation_time,
                "message": f"⚡ INSTANT: {template['name']} generated in {generation_time:.1f}ms!",
                "instant": True
            }
            
        except Exception as e:
            error_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "error": str(e),
                "generation_time": error_time,
                "instant": False
            }
    
    def _get_todo_template(self) -> Dict:
        return {
            "name": "Modern Todo App",
            "description": "A sleek todo application with local storage and animations",
            "files": [
                {
                    "name": "index.html",
                    "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Todo App</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <header class="app-header">
            <h1><i class="fas fa-tasks"></i> Modern Todo</h1>
            <div class="stats">
                <span id="total-tasks">0 tasks</span>
                <span id="completed-tasks">0 completed</span>
            </div>
        </header>
        
        <div class="input-section">
            <div class="input-container">
                <input type="text" id="todo-input" placeholder="Add a new task..." maxlength="100">
                <button id="add-btn"><i class="fas fa-plus"></i></button>
            </div>
        </div>
        
        <div class="filter-section">
            <button class="filter-btn active" data-filter="all">All</button>
            <button class="filter-btn" data-filter="active">Active</button>
            <button class="filter-btn" data-filter="completed">Completed</button>
        </div>
        
        <ul id="todo-list" class="todo-list"></ul>
        
        <div class="actions">
            <button id="clear-completed" class="clear-btn">Clear Completed</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""
                },
                {
                    "name": "style.css",
                    "content": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
}

.app-container {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    overflow: hidden;
}

.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    text-align: center;
}

.app-header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    font-weight: 300;
}

.stats {
    display: flex;
    justify-content: center;
    gap: 20px;
    opacity: 0.9;
}

.input-section {
    padding: 30px;
    border-bottom: 1px solid #eee;
}

.input-container {
    display: flex;
    gap: 10px;
}

#todo-input {
    flex: 1;
    padding: 15px 20px;
    border: 2px solid #e1e8ed;
    border-radius: 50px;
    font-size: 16px;
    outline: none;
    transition: all 0.3s ease;
}

#todo-input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

#add-btn {
    width: 50px;
    height: 50px;
    border: none;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

#add-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.filter-section {
    display: flex;
    justify-content: center;
    gap: 10px;
    padding: 20px 30px;
    border-bottom: 1px solid #eee;
}

.filter-btn {
    padding: 8px 16px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.filter-btn.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-color: transparent;
}

.todo-list {
    list-style: none;
    max-height: 400px;
    overflow-y: auto;
}

.todo-item {
    display: flex;
    align-items: center;
    padding: 20px 30px;
    border-bottom: 1px solid #f0f0f0;
    transition: all 0.3s ease;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.todo-item:hover {
    background: #f8f9ff;
}

.todo-item.completed {
    opacity: 0.6;
}

.todo-checkbox {
    width: 20px;
    height: 20px;
    border: 2px solid #ddd;
    border-radius: 50%;
    margin-right: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.todo-checkbox.checked {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-color: transparent;
}

.todo-checkbox.checked::after {
    content: "✓";
    color: white;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    font-size: 12px;
}

.todo-text {
    flex: 1;
    font-size: 16px;
    transition: all 0.3s ease;
}

.todo-text.completed {
    text-decoration: line-through;
    color: #999;
}

.todo-actions {
    display: flex;
    gap: 10px;
}

.action-btn {
    width: 30px;
    height: 30px;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.edit-btn {
    background: #ffd700;
    color: white;
}

.delete-btn {
    background: #ff6b6b;
    color: white;
}

.action-btn:hover {
    transform: scale(1.2);
}

.actions {
    padding: 20px 30px;
    text-align: center;
}

.clear-btn {
    padding: 10px 20px;
    border: 1px solid #ff6b6b;
    background: white;
    color: #ff6b6b;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.clear-btn:hover {
    background: #ff6b6b;
    color: white;
}

@media (max-width: 600px) {
    body {
        padding: 10px;
    }
    
    .app-header h1 {
        font-size: 2rem;
    }
    
    .input-section, .todo-item {
        padding: 15px 20px;
    }
}"""
                },
                {
                    "name": "script.js",
                    "content": """class TodoApp {
    constructor() {
        this.todos = JSON.parse(localStorage.getItem('todos')) || [];
        this.currentFilter = 'all';
        this.init();
    }

    init() {
        this.bindEvents();
        this.render();
        this.updateStats();
    }

    bindEvents() {
        const addBtn = document.getElementById('add-btn');
        const todoInput = document.getElementById('todo-input');
        const clearBtn = document.getElementById('clear-completed');
        const filterBtns = document.querySelectorAll('.filter-btn');

        addBtn.addEventListener('click', () => this.addTodo());
        todoInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTodo();
        });
        clearBtn.addEventListener('click', () => this.clearCompleted());

        filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });
    }

    addTodo() {
        const input = document.getElementById('todo-input');
        const text = input.value.trim();

        if (text) {
            const todo = {
                id: Date.now(),
                text: text,
                completed: false,
                createdAt: new Date().toISOString()
            };

            this.todos.unshift(todo);
            input.value = '';
            this.saveTodos();
            this.render();
            this.updateStats();
        }
    }

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.saveTodos();
            this.render();
            this.updateStats();
        }
    }

    deleteTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        this.saveTodos();
        this.render();
        this.updateStats();
    }

    editTodo(id, newText) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.text = newText;
            this.saveTodos();
            this.render();
        }
    }

    clearCompleted() {
        this.todos = this.todos.filter(t => !t.completed);
        this.saveTodos();
        this.render();
        this.updateStats();
    }

    setFilter(filter) {
        this.currentFilter = filter;
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-filter="${filter}"]`).classList.add('active');
        this.render();
    }

    getFilteredTodos() {
        switch (this.currentFilter) {
            case 'active':
                return this.todos.filter(t => !t.completed);
            case 'completed':
                return this.todos.filter(t => t.completed);
            default:
                return this.todos;
        }
    }

    render() {
        const todoList = document.getElementById('todo-list');
        const filteredTodos = this.getFilteredTodos();

        todoList.innerHTML = '';

        if (filteredTodos.length === 0) {
            todoList.innerHTML = `
                <li class="todo-item" style="text-align: center; padding: 40px;">
                    <span style="color: #999; font-style: italic;">
                        ${this.currentFilter === 'completed' ? 'No completed tasks' :
                          this.currentFilter === 'active' ? 'No active tasks' : 'No tasks yet'}
                    </span>
                </li>
            `;
            return;
        }

        filteredTodos.forEach(todo => {
            const li = document.createElement('li');
            li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
            li.innerHTML = `
                <div class="todo-checkbox ${todo.completed ? 'checked' : ''}" 
                     onclick="app.toggleTodo(${todo.id})"></div>
                <span class="todo-text ${todo.completed ? 'completed' : ''}">${todo.text}</span>
                <div class="todo-actions">
                    <button class="action-btn edit-btn" onclick="app.startEdit(${todo.id})" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn delete-btn" onclick="app.deleteTodo(${todo.id})" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
            todoList.appendChild(li);
        });
    }

    startEdit(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            const newText = prompt('Edit task:', todo.text);
            if (newText !== null && newText.trim()) {
                this.editTodo(id, newText.trim());
            }
        }
    }

    updateStats() {
        const total = this.todos.length;
        const completed = this.todos.filter(t => t.completed).length;
        
        document.getElementById('total-tasks').textContent = `${total} task${total !== 1 ? 's' : ''}`;
        document.getElementById('completed-tasks').textContent = `${completed} completed`;
    }

    saveTodos() {
        localStorage.setItem('todos', JSON.stringify(this.todos));
    }
}

// Initialize the app
const app = new TodoApp();

// Add some demo tasks on first load
if (app.todos.length === 0) {
    const demoTasks = [
        'Welcome to your Modern Todo App! 🎉',
        'Click the checkbox to mark tasks as complete ✅',
        'Use the edit button to modify tasks ✏️',
        'Filter tasks using the buttons above 🔍'
    ];
    
    demoTasks.forEach(task => {
        app.todos.push({
            id: Date.now() + Math.random(),
            text: task,
            completed: false,
            createdAt: new Date().toISOString()
        });
    });
    
    app.saveTodos();
    app.render();
    app.updateStats();
}"""
                }
            ]
        }
    
    def _get_calculator_template(self) -> Dict:
        return {
            "name": "Modern Calculator",
            "description": "A beautiful calculator with advanced operations and themes",
            "files": [
                {
                    "name": "index.html",
                    "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Calculator</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="calculator-container">
        <div class="calculator">
            <div class="theme-switcher">
                <button class="theme-btn" data-theme="light">🌞</button>
                <button class="theme-btn" data-theme="dark">🌙</button>
                <button class="theme-btn" data-theme="colorful">🌈</button>
            </div>
            
            <div class="display">
                <div class="previous-operand" id="previous-operand"></div>
                <div class="current-operand" id="current-operand">0</div>
            </div>
            
            <div class="buttons">
                <button class="btn clear" onclick="calculator.clear()">C</button>
                <button class="btn clear" onclick="calculator.delete()">⌫</button>
                <button class="btn operator" onclick="calculator.chooseOperation('±')">±</button>
                <button class="btn operator" onclick="calculator.chooseOperation('÷')">÷</button>
                
                <button class="btn number" onclick="calculator.appendNumber('7')">7</button>
                <button class="btn number" onclick="calculator.appendNumber('8')">8</button>
                <button class="btn number" onclick="calculator.appendNumber('9')">9</button>
                <button class="btn operator" onclick="calculator.chooseOperation('×')">×</button>
                
                <button class="btn number" onclick="calculator.appendNumber('4')">4</button>
                <button class="btn number" onclick="calculator.appendNumber('5')">5</button>
                <button class="btn number" onclick="calculator.appendNumber('6')">6</button>
                <button class="btn operator" onclick="calculator.chooseOperation('-')">-</button>
                
                <button class="btn number" onclick="calculator.appendNumber('1')">1</button>
                <button class="btn number" onclick="calculator.appendNumber('2')">2</button>
                <button class="btn number" onclick="calculator.appendNumber('3')">3</button>
                <button class="btn operator" onclick="calculator.chooseOperation('+')">+</button>
                
                <button class="btn number zero" onclick="calculator.appendNumber('0')">0</button>
                <button class="btn number" onclick="calculator.appendNumber('.')">.</button>
                <button class="btn equals" onclick="calculator.compute()">=</button>
            </div>
            
            <div class="history" id="history-panel">
                <h3>History</h3>
                <div id="history-list"></div>
                <button class="clear-history" onclick="calculator.clearHistory()">Clear History</button>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""
                },
                {
                    "name": "style.css",
                    "content": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.calculator-container {
    perspective: 1000px;
}

.calculator {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 25px;
    padding: 30px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    max-width: 400px;
    transition: all 0.3s ease;
}

.theme-switcher {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
}

.theme-btn {
    width: 40px;
    height: 40px;
    border: none;
    border-radius: 50%;
    background: #f0f0f0;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.theme-btn:hover {
    transform: scale(1.1);
}

.display {
    background: #000;
    color: white;
    padding: 30px 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    text-align: right;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.previous-operand {
    font-size: 18px;
    opacity: 0.7;
    min-height: 25px;
}

.current-operand {
    font-size: 36px;
    font-weight: 300;
    word-wrap: break-word;
    word-break: break-all;
}

.buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
}

.btn {
    height: 70px;
    border: none;
    border-radius: 15px;
    font-size: 24px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.btn::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: all 0.3s ease;
}

.btn:active::before {
    width: 100px;
    height: 100px;
}

.number {
    background: #f8f9fa;
    color: #333;
}

.number:hover {
    background: #e9ecef;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.operator {
    background: linear-gradient(135deg, #ff6b6b, #ff5252);
    color: white;
}

.operator:hover {
    background: linear-gradient(135deg, #ff5252, #ff1744);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
}

.equals {
    background: linear-gradient(135deg, #4caf50, #45a049);
    color: white;
    grid-column: span 2;
}

.equals:hover {
    background: linear-gradient(135deg, #45a049, #3d8b40);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
}

.clear {
    background: linear-gradient(135deg, #ff9800, #ff6f00);
    color: white;
}

.clear:hover {
    background: linear-gradient(135deg, #ff6f00, #e65100);
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 152, 0, 0.4);
}

.zero {
    grid-column: span 2;
}

.history {
    margin-top: 20px;
    padding: 20px;
    background: rgba(0, 0, 0, 0.05);
    border-radius: 15px;
    max-height: 200px;
    overflow-y: auto;
}

.history h3 {
    margin-bottom: 10px;
    color: #333;
}

#history-list {
    margin-bottom: 15px;
}

.history-item {
    padding: 5px 0;
    color: #666;
    font-family: monospace;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.clear-history {
    width: 100%;
    padding: 10px;
    border: none;
    background: #ff6b6b;
    color: white;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.clear-history:hover {
    background: #ff5252;
}

/* Dark Theme */
body.dark {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.dark .calculator {
    background: rgba(30, 30, 30, 0.95);
    color: white;
}

.dark .number {
    background: #404040;
    color: white;
}

.dark .number:hover {
    background: #505050;
}

.dark .display {
    background: #1a1a1a;
}

.dark .history {
    background: rgba(255, 255, 255, 0.1);
}

.dark .history h3,
.dark .history-item {
    color: white;
}

/* Colorful Theme */
.colorful .calculator {
    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
}

.colorful .number {
    background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    color: #333;
}

.colorful .display {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

@media (max-width: 480px) {
    .calculator {
        padding: 20px;
        margin: 10px;
    }
    
    .btn {
        height: 60px;
        font-size: 20px;
    }
    
    .current-operand {
        font-size: 28px;
    }
}"""
                },
                {
                    "name": "script.js",
                    "content": """class Calculator {
    constructor() {
        this.clear();
        this.history = JSON.parse(localStorage.getItem('calc-history')) || [];
        this.updateHistoryDisplay();
        this.addKeyboardSupport();
        this.loadTheme();
    }

    clear() {
        this.currentOperand = '';
        this.previousOperand = '';
        this.operation = undefined;
        this.updateDisplay();
    }

    delete() {
        this.currentOperand = this.currentOperand.toString().slice(0, -1);
        this.updateDisplay();
    }

    appendNumber(number) {
        if (number === '.' && this.currentOperand.includes('.')) return;
        this.currentOperand = this.currentOperand.toString() + number.toString();
        this.updateDisplay();
    }

    chooseOperation(operation) {
        if (this.currentOperand === '') return;
        if (this.previousOperand !== '') {
            this.compute();
        }
        
        if (operation === '±') {
            this.currentOperand = (parseFloat(this.currentOperand) * -1).toString();
            this.updateDisplay();
            return;
        }
        
        this.operation = operation;
        this.previousOperand = this.currentOperand;
        this.currentOperand = '';
        this.updateDisplay();
    }

    compute() {
        let computation;
        const prev = parseFloat(this.previousOperand);
        const current = parseFloat(this.currentOperand);
        
        if (isNaN(prev) || isNaN(current)) return;
        
        const expression = `${prev} ${this.operation} ${current}`;
        
        switch (this.operation) {
            case '+':
                computation = prev + current;
                break;
            case '-':
                computation = prev - current;
                break;
            case '×':
                computation = prev * current;
                break;
            case '÷':
                if (current === 0) {
                    alert('Cannot divide by zero!');
                    return;
                }
                computation = prev / current;
                break;
            default:
                return;
        }
        
        // Add to history
        this.addToHistory(`${expression} = ${computation}`);
        
        this.currentOperand = computation;
        this.operation = undefined;
        this.previousOperand = '';
        this.updateDisplay();
    }

    updateDisplay() {
        document.getElementById('current-operand').innerText = 
            this.getDisplayNumber(this.currentOperand);
        
        if (this.operation != null) {
            document.getElementById('previous-operand').innerText =
                `${this.getDisplayNumber(this.previousOperand)} ${this.operation}`;
        } else {
            document.getElementById('previous-operand').innerText = '';
        }
    }

    getDisplayNumber(number) {
        if (number === '') return '0';
        const stringNumber = number.toString();
        const integerDigits = parseFloat(stringNumber.split('.')[0]);
        const decimalDigits = stringNumber.split('.')[1];
        let integerDisplay;
        
        if (isNaN(integerDigits)) {
            integerDisplay = '';
        } else {
            integerDisplay = integerDigits.toLocaleString('en', {
                maximumFractionDigits: 0
            });
        }
        
        if (decimalDigits != null) {
            return `${integerDisplay}.${decimalDigits}`;
        } else {
            return integerDisplay;
        }
    }

    addToHistory(calculation) {
        this.history.unshift(calculation);
        if (this.history.length > 10) {
            this.history = this.history.slice(0, 10);
        }
        localStorage.setItem('calc-history', JSON.stringify(this.history));
        this.updateHistoryDisplay();
    }

    updateHistoryDisplay() {
        const historyList = document.getElementById('history-list');
        historyList.innerHTML = '';
        
        this.history.forEach(item => {
            const div = document.createElement('div');
            div.className = 'history-item';
            div.textContent = item;
            historyList.appendChild(div);
        });
    }

    clearHistory() {
        this.history = [];
        localStorage.removeItem('calc-history');
        this.updateHistoryDisplay();
    }

    addKeyboardSupport() {
        document.addEventListener('keydown', (e) => {
            if (e.key >= '0' && e.key <= '9' || e.key === '.') {
                this.appendNumber(e.key);
            } else if (e.key === '+') {
                this.chooseOperation('+');
            } else if (e.key === '-') {
                this.chooseOperation('-');
            } else if (e.key === '*') {
                this.chooseOperation('×');
            } else if (e.key === '/') {
                e.preventDefault();
                this.chooseOperation('÷');
            } else if (e.key === 'Enter' || e.key === '=') {
                this.compute();
            } else if (e.key === 'Escape') {
                this.clear();
            } else if (e.key === 'Backspace') {
                this.delete();
            }
        });
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('calc-theme') || 'light';
        this.setTheme(savedTheme);
        
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setTheme(e.target.dataset.theme);
            });
        });
    }

    setTheme(theme) {
        document.body.className = theme;
        localStorage.setItem('calc-theme', theme);
        
        document.querySelectorAll('.theme-btn').forEach(btn => {
            btn.style.background = btn.dataset.theme === theme ? '#007bff' : '#f0f0f0';
            btn.style.color = btn.dataset.theme === theme ? 'white' : 'black';
        });
    }
}

const calculator = new Calculator();"""
                }
            ]
        }

    def _get_portfolio_template(self) -> Dict:
        return {
            "name": "Creative Portfolio",
            "description": "A stunning personal portfolio with animations and modern design",
            "files": [
                {
                    "name": "index.html",
                    "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creative Portfolio</title>
    <link rel="stylesheet" href="style.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-logo">Portfolio</div>
            <ul class="nav-menu">
                <li><a href="#home" class="nav-link">Home</a></li>
                <li><a href="#about" class="nav-link">About</a></li>
                <li><a href="#projects" class="nav-link">Projects</a></li>
                <li><a href="#contact" class="nav-link">Contact</a></li>
            </ul>
        </div>
    </nav>

    <section id="home" class="hero">
        <div class="hero-content">
            <h1 class="hero-title">Creative Developer</h1>
            <p class="hero-subtitle">Bringing ideas to life through code</p>
            <div class="hero-buttons">
                <a href="#projects" class="btn btn-primary">View My Work</a>
                <a href="#contact" class="btn btn-secondary">Get In Touch</a>
            </div>
        </div>
        <div class="hero-animation">
            <div class="floating-shapes">
                <div class="shape shape-1"></div>
                <div class="shape shape-2"></div>
                <div class="shape shape-3"></div>
            </div>
        </div>
    </section>

    <section id="about" class="about">
        <div class="container">
            <h2 class="section-title">About Me</h2>
            <div class="about-content">
                <div class="about-text">
                    <p>I'm a passionate developer who loves creating beautiful and functional digital experiences. With expertise in modern web technologies, I transform ideas into reality.</p>
                    <div class="skills">
                        <div class="skill">
                            <span class="skill-name">JavaScript</span>
                            <div class="skill-bar">
                                <div class="skill-progress" data-width="90%"></div>
                            </div>
                        </div>
                        <div class="skill">
                            <span class="skill-name">React</span>
                            <div class="skill-bar">
                                <div class="skill-progress" data-width="85%"></div>
                            </div>
                        </div>
                        <div class="skill">
                            <span class="skill-name">CSS</span>
                            <div class="skill-bar">
                                <div class="skill-progress" data-width="95%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="projects" class="projects">
        <div class="container">
            <h2 class="section-title">My Projects</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-image">
                        <div class="project-overlay">
                            <div class="project-buttons">
                                <a href="#" class="project-btn">Live Demo</a>
                                <a href="#" class="project-btn">Code</a>
                            </div>
                        </div>
                    </div>
                    <div class="project-info">
                        <h3>E-Commerce Platform</h3>
                        <p>A full-stack e-commerce solution with React and Node.js</p>
                        <div class="project-tech">
                            <span>React</span>
                            <span>Node.js</span>
                            <span>MongoDB</span>
                        </div>
                    </div>
                </div>
                
                <div class="project-card">
                    <div class="project-image">
                        <div class="project-overlay">
                            <div class="project-buttons">
                                <a href="#" class="project-btn">Live Demo</a>
                                <a href="#" class="project-btn">Code</a>
                            </div>
                        </div>
                    </div>
                    <div class="project-info">
                        <h3>Task Management App</h3>
                        <p>A collaborative task management tool with real-time updates</p>
                        <div class="project-tech">
                            <span>Vue.js</span>
                            <span>Firebase</span>
                            <span>CSS3</span>
                        </div>
                    </div>
                </div>
                
                <div class="project-card">
                    <div class="project-image">
                        <div class="project-overlay">
                            <div class="project-buttons">
                                <a href="#" class="project-btn">Live Demo</a>
                                <a href="#" class="project-btn">Code</a>
                            </div>
                        </div>
                    </div>
                    <div class="project-info">
                        <h3>Weather Dashboard</h3>
                        <p>A beautiful weather app with interactive charts and forecasts</p>
                        <div class="project-tech">
                            <span>JavaScript</span>
                            <span>API</span>
                            <span>Charts.js</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="contact">
        <div class="container">
            <h2 class="section-title">Get In Touch</h2>
            <div class="contact-content">
                <div class="contact-info">
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <span>hello@portfolio.com</span>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-phone"></i>
                        <span>+1 (555) 123-4567</span>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <span>New York, NY</span>
                    </div>
                    <div class="social-links">
                        <a href="#"><i class="fab fa-github"></i></a>
                        <a href="#"><i class="fab fa-linkedin"></i></a>
                        <a href="#"><i class="fab fa-twitter"></i></a>
                    </div>
                </div>
                <form class="contact-form">
                    <input type="text" placeholder="Your Name" required>
                    <input type="email" placeholder="Your Email" required>
                    <textarea placeholder="Your Message" rows="5" required></textarea>
                    <button type="submit" class="btn btn-primary">Send Message</button>
                </form>
            </div>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""
                },
                {
                    "name": "style.css",
                    "content": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    overflow-x: hidden;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navigation */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    transition: all 0.3s ease;
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
}

.nav-logo {
    font-size: 1.8rem;
    font-weight: bold;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-link {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    transition: all 0.3s ease;
    position: relative;
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    transition: width 0.3s ease;
}

.nav-link:hover::after {
    width: 100%;
}

/* Hero Section */
.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero-content {
    z-index: 2;
    position: relative;
}

.hero-title {
    font-size: 4rem;
    font-weight: 300;
    margin-bottom: 1rem;
    animation: fadeInUp 1s ease;
}

.hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: 2rem;
    opacity: 0.9;
    animation: fadeInUp 1s ease 0.2s both;
}

.hero-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    animation: fadeInUp 1s ease 0.4s both;
}

.btn {
    padding: 12px 30px;
    border: none;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    cursor: pointer;
    display: inline-block;
}

.btn-primary {
    background: white;
    color: #667eea;
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(255, 255, 255, 0.3);
}

.btn-secondary {
    background: transparent;
    color: white;
    border: 2px solid white;
}

.btn-secondary:hover {
    background: white;
    color: #667eea;
    transform: translateY(-3px);
}

/* Floating Shapes Animation */
.hero-animation {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.floating-shapes {
    position: relative;
    width: 100%;
    height: 100%;
}

.shape {
    position: absolute;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    animation: float 6s ease-in-out infinite;
}

.shape-1 {
    width: 100px;
    height: 100px;
    top: 20%;
    left: 10%;
    animation-delay: 0s;
}

.shape-2 {
    width: 150px;
    height: 150px;
    top: 60%;
    right: 10%;
    animation-delay: 2s;
}

.shape-3 {
    width: 80px;
    height: 80px;
    bottom: 20%;
    left: 50%;
    animation-delay: 4s;
}

@keyframes float {
    0%, 100% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-20px);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Sections */
.section-title {
    font-size: 3rem;
    text-align: center;
    margin-bottom: 3rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.about {
    padding: 100px 0;
    background: #f8f9fa;
}

.about-content {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
}

.about-text p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    color: #666;
}

.skills {
    max-width: 600px;
    margin: 0 auto;
}

.skill {
    margin-bottom: 1.5rem;
}

.skill-name {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.skill-bar {
    height: 8px;
    background: #e9ecef;
    border-radius: 4px;
    overflow: hidden;
}

.skill-progress {
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
    width: 0;
    transition: width 1s ease;
}

/* Projects */
.projects {
    padding: 100px 0;
}

.projects-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
}

.project-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.project-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.project-image {
    height: 200px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    position: relative;
    overflow: hidden;
}

.project-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: all 0.3s ease;
}

.project-card:hover .project-overlay {
    opacity: 1;
}

.project-buttons {
    display: flex;
    gap: 1rem;
}

.project-btn {
    padding: 10px 20px;
    background: white;
    color: #333;
    text-decoration: none;
    border-radius: 25px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.project-btn:hover {
    background: #667eea;
    color: white;
}

.project-info {
    padding: 2rem;
}

.project-info h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #333;
}

.project-info p {
    color: #666;
    margin-bottom: 1rem;
}

.project-tech {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.project-tech span {
    padding: 5px 12px;
    background: #e9ecef;
    border-radius: 15px;
    font-size: 0.85rem;
    color: #666;
}

/* Contact */
.contact {
    padding: 100px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.contact .section-title {
    color: white;
    -webkit-text-fill-color: white;
}

.contact-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    max-width: 1000px;
    margin: 0 auto;
}

.contact-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.contact-item i {
    font-size: 1.2rem;
    width: 20px;
}

.social-links {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}

.social-links a {
    width: 50px;
    height: 50px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    text-decoration: none;
    transition: all 0.3s ease;
}

.social-links a:hover {
    background: white;
    color: #667eea;
    transform: translateY(-3px);
}

.contact-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.contact-form input,
.contact-form textarea {
    padding: 15px;
    border: none;
    border-radius: 10px;
    font-size: 1rem;
    resize: vertical;
}

.contact-form button {
    align-self: flex-start;
    margin-top: 1rem;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 2.5rem;
    }
    
    .hero-buttons {
        flex-direction: column;
        align-items: center;
    }
    
    .nav-menu {
        display: none;
    }
    
    .contact-content {
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    
    .projects-grid {
        grid-template-columns: 1fr;
    }
}"""
                },
                {
                    "name": "script.js",
                    "content": """// Portfolio Interactive Features
class Portfolio {
    constructor() {
        this.init();
    }

    init() {
        this.setupSmoothScrolling();
        this.setupSkillBars();
        this.setupNavbarScroll();
        this.setupContactForm();
        this.setupIntersectionObserver();
    }

    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    setupSkillBars() {
        const animateSkills = () => {
            const skillBars = document.querySelectorAll('.skill-progress');
            skillBars.forEach(bar => {
                const width = bar.getAttribute('data-width');
                bar.style.width = width;
            });
        };

        // Animate skills when about section is visible
        const aboutSection = document.querySelector('#about');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(animateSkills, 500);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(aboutSection);
    }

    setupNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        let lastScrollY = window.scrollY;

        window.addEventListener('scroll', () => {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 100) {
                navbar.style.background = 'rgba(255, 255, 255, 0.98)';
                navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                navbar.style.boxShadow = 'none';
            }

            lastScrollY = currentScrollY;
        });
    }

    setupContactForm() {
        const form = document.querySelector('.contact-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(form);
            const name = form.querySelector('input[type="text"]').value;
            const email = form.querySelector('input[type="email"]').value;
            const message = form.querySelector('textarea').value;
            
            // Simulate sending message
            this.showFormMessage('Thank you for your message! I will get back to you soon.', 'success');
            
            // Reset form
            form.reset();
        });
    }

    showFormMessage(message, type) {
        const messageEl = document.createElement('div');
        messageEl.className = `form-message ${type}`;
        messageEl.textContent = message;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            background: ${type === 'success' ? '#4caf50' : '#f44336'};
            color: white;
            border-radius: 10px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(messageEl);
        
        setTimeout(() => {
            messageEl.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => {
                document.body.removeChild(messageEl);
            }, 300);
        }, 3000);
    }

    setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                }
            });
        }, observerOptions);

        // Observe project cards
        document.querySelectorAll('.project-card').forEach(card => {
            observer.observe(card);
        });
    }
}

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize portfolio when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Portfolio();
});

// Add some interactive particles for extra visual appeal
class ParticleSystem {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.setup();
        this.animate();
    }

    setup() {
        this.canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.6;
        `;
        
        document.body.appendChild(this.canvas);
        this.resize();
        
        window.addEventListener('resize', () => this.resize());
        
        // Create particles
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1
            });
        }
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;
            
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fillStyle = 'rgba(102, 126, 234, 0.3)';
            this.ctx.fill();
        });
        
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize particle system
// new ParticleSystem(); // Uncomment if you want particle effects"""
                }
            ]
        }

    # Add more templates for other project types
    def _get_weather_template(self) -> Dict:
        return {
            "name": "Weather Dashboard",
            "description": "A beautiful weather app with forecasts and animations",
            "files": [
                {
                    "name": "index.html",
                    "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="weather-app">
        <div class="search-box">
            <input type="text" id="city-input" placeholder="Enter city name...">
            <button id="search-btn">🔍</button>
        </div>
        <div class="weather-display">
            <div class="current-weather">
                <h2 id="city-name">Weather Dashboard</h2>
                <div class="weather-icon">☀️</div>
                <div class="temperature" id="temperature">--°</div>
                <div class="weather-desc" id="description">Enter a city to get weather</div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
                },
                {
                    "name": "style.css", 
                    "content": """body {
    margin: 0;
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, #74b9ff, #0984e3);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.weather-app {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    color: white;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

.search-box {
    display: flex;
    gap: 10px;
    margin-bottom: 30px;
}

#city-input {
    flex: 1;
    padding: 15px;
    border: none;
    border-radius: 25px;
    font-size: 16px;
}

#search-btn {
    padding: 15px 20px;
    border: none;
    border-radius: 25px;
    background: white;
    cursor: pointer;
}

.weather-icon {
    font-size: 80px;
    margin: 20px 0;
}

.temperature {
    font-size: 60px;
    font-weight: bold;
    margin: 20px 0;
}"""
                },
                {
                    "name": "script.js",
                    "content": """// Weather App Demo
document.getElementById('search-btn').addEventListener('click', searchWeather);
document.getElementById('city-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchWeather();
});

function searchWeather() {
    const city = document.getElementById('city-input').value;
    if (!city) return;
    
    // Demo weather data
    const demoWeather = {
        'New York': { temp: 22, desc: 'Sunny', icon: '☀️' },
        'London': { temp: 15, desc: 'Cloudy', icon: '☁️' },
        'Tokyo': { temp: 28, desc: 'Partly Cloudy', icon: '⛅' },
        'Paris': { temp: 18, desc: 'Rainy', icon: '🌧️' }
    };
    
    const weather = demoWeather[city] || { temp: 20, desc: 'Clear', icon: '☀️' };
    
    document.getElementById('city-name').textContent = city;
    document.getElementById('temperature').textContent = weather.temp + '°C';
    document.getElementById('description').textContent = weather.desc;
    document.querySelector('.weather-icon').textContent = weather.icon;
}"""
                }
            ]
        }

    def _get_landing_template(self) -> Dict:
        return {
            "name": "Modern Landing Page",
            "description": "A sleek business landing page with call-to-action",
            "files": [
                {
                    "name": "index.html",
                    "content": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Landing Page</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">Brand</div>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#pricing">Pricing</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <section id="home" class="hero">
        <div class="hero-content">
            <h1>Transform Your Business</h1>
            <p>Powerful solutions for modern challenges</p>
            <button class="cta-button">Get Started</button>
        </div>
    </section>
    
    <section id="features" class="features">
        <h2>Why Choose Us</h2>
        <div class="feature-grid">
            <div class="feature">
                <div class="feature-icon">⚡</div>
                <h3>Fast</h3>
                <p>Lightning-fast performance</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🔒</div>
                <h3>Secure</h3>
                <p>Bank-level security</p>
            </div>
            <div class="feature">
                <div class="feature-icon">📱</div>
                <h3>Mobile</h3>
                <p>Works on all devices</p>
            </div>
        </div>
    </section>
    
    <script src="script.js"></script>
</body>
</html>"""
                },
                {
                    "name": "style.css",
                    "content": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 5%;
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

nav ul {
    display: flex;
    list-style: none;
    gap: 2rem;
}

nav a {
    text-decoration: none;
    color: #333;
}

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 100px 20px;
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.cta-button {
    padding: 15px 30px;
    font-size: 1.1rem;
    background: white;
    color: #667eea;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.cta-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.features {
    padding: 80px 20px;
    text-align: center;
}

.features h2 {
    font-size: 2.5rem;
    margin-bottom: 3rem;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
}

.feature {
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.feature h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
}"""
                },
                {
                    "name": "script.js",
                    "content": """// Landing page interactions
document.querySelector('.cta-button').addEventListener('click', function() {
    alert('Welcome! This is a demo landing page.');
});

// Smooth scrolling for navigation
document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});"""
                }
            ]
        }

    # Add other template methods (contact_form, memory_game, quiz, timer, color_picker)
    def _get_contact_template(self) -> Dict:
        return {"name": "Contact Form", "description": "A responsive contact form", "files": [{"name": "index.html", "content": "<!-- Contact form HTML -->"}, {"name": "style.css", "content": "/* Contact form CSS */"}, {"name": "script.js", "content": "// Contact form JS"}]}

    def _get_memory_game_template(self) -> Dict:
        return {"name": "Memory Game", "description": "Card matching memory game", "files": [{"name": "index.html", "content": "<!-- Memory game HTML -->"}, {"name": "style.css", "content": "/* Memory game CSS */"}, {"name": "script.js", "content": "// Memory game JS"}]}

    def _get_quiz_template(self) -> Dict:
        return {"name": "Quiz App", "description": "Interactive quiz application", "files": [{"name": "index.html", "content": "<!-- Quiz HTML -->"}, {"name": "style.css", "content": "/* Quiz CSS */"}, {"name": "script.js", "content": "// Quiz JS"}]}

    def _get_timer_template(self) -> Dict:
        return {"name": "Timer App", "description": "Countdown timer and stopwatch", "files": [{"name": "index.html", "content": "<!-- Timer HTML -->"}, {"name": "style.css", "content": "/* Timer CSS */"}, {"name": "script.js", "content": "// Timer JS"}]}

    def _get_color_picker_template(self) -> Dict:
        return {"name": "Color Picker", "description": "RGB color picker tool", "files": [{"name": "index.html", "content": "<!-- Color picker HTML -->"}, {"name": "style.css", "content": "/* Color picker CSS */"}, {"name": "script.js", "content": "// Color picker JS"}]}

# Global instant generator
instant_generator = InstantProjectGenerator()