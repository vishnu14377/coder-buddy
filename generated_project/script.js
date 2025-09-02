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
    if (name === '' || email === '' || message === '') {
        alert('Please fill in all fields.');
        return;
    }

    // Check if email is valid
    if (!email.includes('@')) {
        alert('Invalid email address.');
        return;
    }

    // Get the form data
    var formData = {
        name: name,
        email: email,
        message: message
    };

    // Send data to server for storage
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
});
