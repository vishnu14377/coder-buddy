function validateEmail(email) {
  // Regular expression for email validation
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function validateForm() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const message = document.getElementById("message").value;

  let isValid = true;

  // Name validation
  if (name.trim() === "") {
    document.getElementById("nameError").textContent = "Name is required";
    isValid = false;
  } else {
    document.getElementById("nameError").textContent = "";
  }

  // Email validation
  if (email.trim() === "") {
    document.getElementById("emailError").textContent = "Email is required";
    isValid = false;
  } else if (!validateEmail(email)) {
    document.getElementById("emailError").textContent = "Invalid email format";
    isValid = false;
  } else {
    document.getElementById("emailError").textContent = "";
  }

  // Message validation
  if (message.trim() === "") {
    document.getElementById("messageError").textContent = "Message is required";
    isValid = false;
  } else {
    document.getElementById("messageError").textContent = "";
  }

  return isValid;
}

function handleSubmit(event) {
  event.preventDefault();

  if (validateForm()) {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;

    //Simulate sending data to server.  Replace with actual fetch or AJAX call.
    const formData = { name, email, message };
    console.log("Form data:", formData);


    // Display success message
    document.getElementById("submitMessage").textContent = "Message sent successfully!";
    document.getElementById("submitMessage").style.color = "green";


  } else {
    // Display error message (already handled by validateForm)

  }
}


document.getElementById('contactForm').addEventListener('submit', handleSubmit);