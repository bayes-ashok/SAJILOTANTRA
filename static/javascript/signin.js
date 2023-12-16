document.addEventListener('DOMContentLoaded', function () {
  var alertElement = document.getElementById('alert-1');
  var closeButton = alertElement.querySelector('[data-dismiss-target="#alert-1"]');
  
  // Check if "Remember Me" is set in local storage
  var rememberMeChecked = localStorage.getItem('rememberMe') === 'true';

  // Set the checkbox state based on the stored preference
  var rememberMeCheckbox = document.getElementById('remember');
  rememberMeCheckbox.checked = rememberMeChecked;

  // Close the alert when the cross is clicked
  closeButton.addEventListener('click', function () {
    alertElement.style.display = 'none';
  });

  // Fade away the alert after 5 seconds if the user does not click the cross
  setTimeout(function () {
    alertElement.style.transition = 'opacity 1s ease-out';
    alertElement.style.opacity = 0;
    setTimeout(function () {
      alertElement.style.display = 'none';
    }, 1000);
  }, 5000);

  // Remember Me functionality
  rememberMeCheckbox.addEventListener('change', function () {
    // Store the "Remember Me" preference in local storage
    localStorage.setItem('rememberMe', this.checked);
  });
});
function togglePassword() {
  var passwordField = document.getElementById("pass1");
  var eyeIcon = document.getElementById("eyeIcon");

  if (passwordField.type === "password") {
    passwordField.type = "text";
    eyeIcon.classList.remove("bi-eye");
    eyeIcon.classList.add("bi-eye-slash");
  } else {
    passwordField.type = "password";
    eyeIcon.classList.remove("bi-eye-slash");
    eyeIcon.classList.add("bi-eye");
  }
}