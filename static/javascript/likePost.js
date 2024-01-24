function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// function updateLikeButtonState(likeButton, isLiked) {
//     likeButton.classList.toggle('liked', isLiked);
//     likeButton.classList.toggle('not-liked', !isLiked);
// }
function updateLikeButtonState(likeButton, isLiked) {
    const likeIcon = likeButton.querySelector('.like-icon');
    if (isLiked) {
        likeIcon.style.fill = "red"; // Directly setting SVG fill color for liked
    } else {
        likeIcon.style.fill = "green"; // Directly setting SVG fill color for not liked
    }
}

function likePost(postId) {
    var csrfToken = getCookie('csrftoken');

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
        let likeButton = document.querySelector('.like-button[data-post-id="' + postId + '"]');
        let likeCountElement = document.getElementById('like-count-' + postId);

        if (data.message === 'Post liked successfully' || data.message === 'Post unliked successfully') {
            // Toggle liked state and update like count
            likeCountElement.innerText = data.like_count;
            updateLikeButtonState(likeButton, data.is_liked);
        } else {
            alert(data.message); // Handle other messages
        }
    })
    .catch(error => console.error('Error:', error));
}

// Event listener for DOM content loaded
document.addEventListener('DOMContentLoaded', function() {
    // Attach event listener to like buttons
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', function() {
            let postId = this.getAttribute('data-post-id');
            likePost(postId);
        });
    });
});
