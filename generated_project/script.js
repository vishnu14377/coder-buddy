// Function to validate name
function validateName(name) {
    if (name === '' || name.length < 2) {
        alert('Please enter a valid name.');
        return false;
    } else {
        return true;
    }
}

// Function to validate email
function validateEmail(email) {
    if (!email.includes('@')) {
        alert('Invalid email address.');
        return false;
    } else {
        return true;
    }
}

// Function to validate message
function validateMessage(message) {
    if (message === '' || message.length < 10) {
        alert('Please enter a valid message.');
        return false;
    } else {
        return true;
    }
}

// Get the form element
var form = document.getElementById('contact-form');

// Add event listener to the form
form.addEventListener('submit', function(event) {
    // Prevent default form submission
    event.preventDefault();

    // Validate form fields
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var message = document.getElementById('message').value;

    // Check if fields are not empty
    if (!validateName(name) || !validateEmail(email) || !validateMessage(message)) {
        return;
    }

    // Get the form data
    var formData = {
        name: name,
        email: email,
        message: message
    };

    // Function to perform addition
    function add(num1, num2) {
        if (typeof num1 !== 'number' || typeof num2 !== 'number') {
            alert('Invalid input. Please enter numbers only.');
            return;
        }
        return num1 + num2;
    }

    // Function to perform subtraction
    function subtract(num1, num2) {
        if (typeof num1 !== 'number' || typeof num2 !== 'number') {
            alert('Invalid input. Please enter numbers only.');
            return;
        }
        if (num2 > num1) {
            alert('Subtraction result would be negative.');
            return;
        }
        return num1 - num2;
    }

    // Function to perform multiplication
    function multiply(num1, num2) {
        if (typeof num1 !== 'number' || typeof num2 !== 'number') {
            alert('Invalid input. Please enter numbers only.');
            return;
        }
        return num1 * num2;
    }

    // Function to perform division
    function divide(num1, num2) {
        if (typeof num1 !== 'number' || typeof num2 !== 'number') {
            alert('Invalid input. Please enter numbers only.');
            return;
        }
        if (num2 === 0) {
            alert('Cannot divide by zero.');
            return;
        }
        return num1 / num2;
    }

    // Get user input for numbers
    var num1 = document.getElementById('num1').value;
    var num2 = document.getElementById('num2').value;

    // Check if fields are not empty
    if (num1 === '' || num2 === '') {
        alert('Please enter both numbers.');
        return;
    }

    // Perform calculation based on user choice
    var result;
    switch(document.getElementById('calculation').value) {
        case 'add':
            result = add(parseFloat(num1), parseFloat(num2));
            break;
        case 'subtract':
            result = subtract(parseFloat(num1), parseFloat(num2));
            break;
        case 'multiply':
            result = multiply(parseFloat(num1), parseFloat(num2));
            break;
        case 'divide':
            result = divide(parseFloat(num1), parseFloat(num2));
            break;
        default:
            alert('Invalid calculation choice.');
            return;
    }

    // Store result
    var storedResult = result;

    // Create a heading text element
    var heading = document.createElement('h1');
    heading.textContent = 'Result: ' + result;

    // Append the heading text to the form
    form.appendChild(heading);

    // Clear the form fields
    form.reset();
}

// Function to update the heading text on page load
function updateHeadingText() {
    // Get the heading element
    var heading = document.getElementById('heading');

    // Check if the heading element exists
    if (heading) {
        // Update the heading text
        heading.textContent = 'Welcome to our website!';
    }
}

// Add event listener to the page load
window.addEventListener('load', updateHeadingText);

// Variable to store result
var result = storedResult;