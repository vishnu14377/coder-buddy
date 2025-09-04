class Calculator {
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

const calculator = new Calculator();