function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Search for the CSRF token cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Function to handle liking a post
function likePost(postId) {
    // Retrieve CSRF token
    var csrfToken = getCookie('csrftoken');

    // Use CSRF token in fetch request
    fetch(`/post/${postId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'post_id': postId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Post liked successfully') {
            let likeCountElement = document.getElementById('like-count-' + postId);
            likeCountElement.innerText = parseInt(likeCountElement.innerText) + 1;
        } else {
            alert(data.message); // Handle other messages
        }
    })
    .catch(error => console.error('Error:', error));
}

// Event listener after DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Attach event listener to like buttons
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            likePost(this.getAttribute('data-post-id'));
        });
    });
});