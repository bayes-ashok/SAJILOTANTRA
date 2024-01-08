// For Hamburger Menu
const navLinks = document.querySelector('.nav-links')
function onToggleMenu(e) {
    const isOpen = navLinks.classList.contains('top-[9%]');

    if (isOpen) {
        e.name = 'menu';
    } else {
        e.name = 'close';
    }

    navLinks.classList.toggle('top-[9%]');
}

// {% comment %} For Profile Container {% endcomment %}
const profileContainer = document.getElementById('profileContainer');
const profileDropdown = document.getElementById('profileDropdown');

profileContainer.addEventListener('click', function (event) {
event.stopPropagation(); // Stop the click event from reaching the window
profileDropdown.classList.toggle('hidden');
});

// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function () {
if (!profileDropdown.classList.contains('hidden')) {
    profileDropdown.classList.add('hidden');
}
});

// {% comment %} For Notifications Dropdown {% endcomment %}
const notificationButton = document.getElementById('notificationButton');
const notificationDropdown = document.getElementById('notification-dropdown');

notificationButton.addEventListener('click', function (event) {
event.stopPropagation(); // Stop the click event from reaching the window
notificationDropdown.classList.toggle('hidden');
});

// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function () {
if (!notificationDropdown.classList.contains('hidden')) {
    notificationDropdown.classList.add('hidden');
}
});

// Create Pop-up
document.addEventListener("DOMContentLoaded", function(event) {
document.getElementById('defaultModalButton').click();
});

// For Create Post Modal
const createToggle = document.getElementById('createPostToggle');
const createModal = document.getElementById('createPostModal');

createModal.addEventListener('click', function (event) {
event.stopPropagation(); // Stop the click event from reaching the window
createModal.classList.toggle('hidden');
});

// Close the dropdown if the user clicks outside of it
window.addEventListener('click', function () {
if (!createModal.classList.contains('hidden')) {
    createModal.classList.add('hidden');
}
});

// Post Images 
