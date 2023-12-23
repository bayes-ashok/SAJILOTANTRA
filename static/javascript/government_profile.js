document.addEventListener('DOMContentLoaded', function() {
    // For Profile Container
    const profileContainer = document.getElementById('profileContainer');
    const profileDropdown = document.getElementById('profileDropdown');

    profileContainer.addEventListener('click', function(event) {
        event.stopPropagation(); // Stop the click event from reaching the window
        profileDropdown.classList.toggle('hidden');
    });

    // For Notifications Dropdown
    const notificationButton = document.getElementById('notificationButton');
    const notificationDropdown = document.getElementById('notification-dropdown');

    notificationButton.addEventListener('click', function(event) {
        event.stopPropagation(); // Stop the click event from reaching the window
        notificationDropdown.classList.toggle('hidden');
    });

    // Close the dropdowns if the user clicks outside of them
    window.addEventListener('click', function() {
        if (!profileDropdown.classList.contains('hidden')) {
            profileDropdown.classList.add('hidden');
        }
        if (!notificationDropdown.classList.contains('hidden')) {
            notificationDropdown.classList.add('hidden');
        }
    });
});
