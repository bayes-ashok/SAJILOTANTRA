// Wait for the DOM to be ready
document.addEventListener("DOMContentLoaded", function () {
    // Get all elements with the data-dismiss-target attribute
    var dismissButtons = document.querySelectorAll('[data-dismiss-target]');

    // Add click event listeners to each button
    dismissButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            // Get the target element to be dismissed
            var targetId = button.getAttribute('data-dismiss-target');
            var targetElement = document.getElementById(targetId);

            // Check if the target element exists
            if (targetElement) {
                // Close the menu by hiding the target element
                targetElement.style.display = 'none';
            }
        });
    });
});