// For Hamburger Menu
const navLinks = document.querySelector('.nav-links');

function onToggleMenu(e) {
  const isOpen = navLinks.classList.contains('top-[9%]');

  if (isOpen) {
    e.setAttribute('name', 'menu');
  } else {
    e.setAttribute('name', 'close');
  }

  navLinks.classList.toggle('top-[9%]');
}

// For Profile Container
const profileContainer = document.getElementById('profileContainer');
const profileDropdown = document.getElementById('profileDropdown');

profileContainer.addEventListener('click', function (event) {
  event.stopPropagation();
  profileDropdown.classList.toggle('hidden');
});

window.addEventListener('click', function () {
  if (!profileDropdown.classList.contains('hidden')) {
    profileDropdown.classList.add('hidden');
  }
});

// For Notifications Dropdown
const notificationButton = document.getElementById('notificationButton');
const notificationDropdown = document.getElementById('notification-dropdown');

notificationButton.addEventListener('click', function (event) {
  event.stopPropagation();
  notificationDropdown.classList.toggle('hidden');
});

window.addEventListener('click', function () {
  if (!notificationDropdown.classList.contains('hidden')) {
    notificationDropdown.classList.add('hidden');
  }
});

// Create Pop-up
document.addEventListener("DOMContentLoaded", function (event) {
  document.getElementById('defaultModalButton').click();
});

// For Create Post Modal
const createToggle = document.getElementById('createPostToggle');
const createModal = document.getElementById('createPostModal');

createToggle.addEventListener('click', function (event) {
  event.stopPropagation();
  createModal.classList.toggle('hidden');
});

window.addEventListener('click', function () {
  if (!createModal.classList.contains('hidden')) {
    createModal.classList.add('hidden');
  }
});
