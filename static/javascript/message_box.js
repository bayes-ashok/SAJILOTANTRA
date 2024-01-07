// JavaScript to display the success message
function showSuccessMessage(message) {
    var messageContainer = document.getElementById('message-container');
    messageContainer.innerText = message;
    messageContainer.style.display = 'block';
    
    // Automatically hide the message after a certain time (e.g., 5 seconds)
    setTimeout(function() {
        messageContainer.style.display = 'none';
    }, 5000); // 5000 milliseconds (5 seconds)
}
