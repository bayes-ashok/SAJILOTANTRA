document.addEventListener('DOMContentLoaded', function () {
  var alertElement = document.getElementById('alert-1');
  var closeButton = alertElement.querySelector('[data-dismiss-target="#alert-1"]');
  var usernameInput = document.getElementById("username");
  var passwordInput = document.getElementById("pass1");
  const rememberMeCheckbox = document.getElementById("remember");

  // Load stored "Remember Me" data from local storage
  const storedData = localStorage.getItem("rememberMeData");
  if (storedData) {
    const data = JSON.parse(storedData);
    usernameInput.value = data.email;
    passwordInput.value = data.password;
    rememberMeCheckbox.checked = true;
  }

  // Check if "Remember Me" is checked and save data to local storage
  rememberMeCheckbox.addEventListener('change', function () {
    if (rememberMeCheckbox.checked) {
      const rememberMeData = JSON.stringify({ email: usernameInput.value, password: passwordInput.value });
      localStorage.setItem("rememberMeData", rememberMeData);
    } else {
      localStorage.removeItem("rememberMeData");
    }
  });

  // Close the alert when the close button is clicked
  closeButton.addEventListener('click', function () {
    alertElement.style.display = 'none';
  });

  // Fade away the alert after 5 seconds if the user does not click the close button
  setTimeout(function () {
    alertElement.style.transition = 'opacity 1s ease-out';
    alertElement.style.opacity = 0;
    setTimeout(function () {
      alertElement.style.display = 'none';
    }, 1000);
  }, 5000);
});

function togglePassword() {
  var passwordField = document.getElementById("pass1");
  var eyeIcon = document.getElementById("eyeIcon");

  if (passwordField.type === "password") {
    passwordField.type = "text";
    eyeIcon.classList.remove("fa-eye");
    eyeIcon.classList.add("fa-eye-slash");
  } else {
    passwordField.type = "password";
    eyeIcon.classList.remove("fa-eye-slash");
    eyeIcon.classList.add("fa-eye");
  }
}

document.addEventListener("DOMContentLoaded", function() {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function validateEmail() {
      const emailInput = document.getElementById('email');
      const emailWarning = document.getElementById('emailWarningSignUp');

      if (!emailPattern.test(emailInput.value)) {
          emailWarning.textContent = 'Please enter a valid email address.';
          return false;
      } else {
          emailWarning.textContent = '';
          return true;
      }
  }

  function validatePassword() {
      const pass1 = document.getElementById('pass1').value;
      const pass2 = document.getElementById('pass2').value;
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;
      const passwordWarning = document.getElementById('passwordWarningSignUp');
      const confirmPasswordWarning = document.getElementById('confirmPasswordWarningSignUp');

      if (pass1.length < 8 || !passwordRegex.test(pass1)) {
          passwordWarning.textContent = 'Password must be at least 8 characters and contain at least one uppercase, one lowercase, one digit, and one special character.';
          return false;
      } else {
          passwordWarning.textContent = '';
      }

      if (pass1 !== pass2) {
          confirmPasswordWarning.textContent = 'Passwords do not match.';
          return false;
      } else {
          confirmPasswordWarning.textContent = '';
      }

      return true;
  }

  function clearEmailWarning() {
      const emailWarning = document.getElementById('emailWarningSignUp');
      emailWarning.textContent = '';
  }

  function togglePassword() {
      const pass1 = document.getElementById('pass1');
      const pass2 = document.getElementById('pass2');
      const eyeIcon = document.getElementById('eyeIcon');

      if (pass1.type === "password") {
          pass1.type = "text";
          pass2.type = "text";
          eyeIcon.classList.add('opacity-0');
      } else {
          pass1.type = "password";
          pass2.type = "password";
          eyeIcon.classList.remove('opacity-0');
      }
  }

  document.getElementById('signup').addEventListener('submit', function(event) {
      if (!validatePassword()) {
          event.preventDefault();
      }
  });
});

