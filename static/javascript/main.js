//validation in signup
document.addEventListener("DOMContentLoaded", function () {
  const registerForm = document.getElementById("signup-form");
  const nameInput = document.getElementById("fname");
  const lastInput = document.getElementById("lname");
  const emailInput = document.getElementById("username");
  const passwordInput = document.getElementById("pass1");
  const confirmPasswordInput = document.getElementById("pass2");
  const emailWarningSignUp = document.getElementById("emailWarningSignUp");
  const passwordWarningSignUp = document.getElementById("passwordWarningSignUp");
  const confirmPasswordWarningSignUp = document.getElementById("confirmPasswordWarningSignUp");
  const nameWarningSignUp = document.getElementById("nameWarningSignUp");
  const lnameWarningSignUp = document.getElementById("lnameWarningSignUp");

  // // Validate an email address
  function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  // Validate a strong password
  function isValidStrongPassword(password) {
    const strongPasswordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).{8,}$/;
    return strongPasswordRegex.test(password);
  }

  // Input event listener to the email field for real-time validation
  emailInput.addEventListener("input", function () {
    const email = emailInput.value;
    if (!isValidEmail(email)) {
      emailWarningSignUp.innerText = "Please enter a valid email address.";
      emailWarningSignUp.style.color = "red";
    } else {
      emailWarningSignUp.innerText = "";
    }
  });

  // Input event listener to the password field for real-time validation
  passwordInput.addEventListener("input", function () {
    const password = passwordInput.value;
    if (!isValidStrongPassword(password)) {
      passwordWarningSignUp.innerText = "Password must be strong (at least 8 characters with uppercase, lowercase, digits, and at least one special character among \"@\", \"#\", \"$\", \"%\", \"^\", \"&\", or \"+\").";
      passwordWarningSignUp.style.color = "red";
    } else {
      passwordWarningSignUp.innerText = "";
    }
  });






  // Click event listener to the "Register" button
  document.getElementById("registerButton").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default form submission

    const name = nameInput.value;
    const lname = lastInput.value;
    const email = emailInput.value;
    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    

    

    // Email validation
    if (!isValidEmail(email)) {
      emailWarningSignUp.innerText = "Please enter a valid email address.";
      emailWarningSignUp.style.color = "red";
      return;
    } else {
      emailWarningSignUp.innerText = "";
    }

    // Password and confirm password match
    if (password !== confirmPassword) {
      confirmPasswordWarningSignUp.innerText = "Passwords do not match.";
      confirmPasswordWarningSignUp.style.color = "red";
      return;
    } else {
      confirmPasswordWarningSignUp.innerText = "";
    }

    // Password validation
    if (!isValidStrongPassword(password)) {
      passwordWarningSignUp.innerText = "Password must be strong (at least 8 characters with uppercase, lowercase, digits, and at least one special character among \"@\", \"#\", \"$\", \"%\", \"^\", \"&\", or \"+\").";
      passwordWarningSignUp.style.color = "red";
      return;
    } else {
      passwordWarningSignUp.innerText = "";
    }

  });
});
