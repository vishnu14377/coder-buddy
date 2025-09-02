// Write the JavaScript content to the file
write_file('script.js', `// Import the necessary libraries
import { read_file, write_file } from './tools.js';

// Define a function to display a message in the HTML page
function displayMessage(message) {
  const msgElement = document.getElementById('message');
  msgElement.innerText = message;
}

// Add an event listener to display a message when the button is clicked
const button = document.getElementById('button');
button.addEventListener('click', () => displayMessage('Hello, World!'));
`);