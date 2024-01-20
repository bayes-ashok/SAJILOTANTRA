// Add this script to handle reporting
document.addEventListener('DOMContentLoaded', function () {
    const reportButtons = document.querySelectorAll('.report-btn');

    reportButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.getAttribute('data-post-id');
            const reason = prompt('Please provide a reason for reporting this post:');

            if (reason !== null && reason !== '') {
                // Send an AJAX request to report the post
                fetch('/report-post/' + postId + '/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ reason: reason }),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Post reported successfully. Thank you for your feedback.');
                        } else {
                            alert('Failed to report the post. Please try again.');
                        }
                    })
                    .catch(error => console.error('Error:', error));
            }
        });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Search for a name/value pair with the given name
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
