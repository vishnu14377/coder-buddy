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

    // Create a heading text element
    var heading = document.createElement('h1');
    heading.textContent = 'Form Submitted Successfully!';

    // Append the heading text to the form
    form.appendChild(heading);

    // Clear the form fields
    form.reset();
});