function reportPost(postId) {
    // Implement your reporting logic here
    console.log('Reporting post', postId);

    // Make an AJAX request to report the post
    fetch('/report_post/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),  // Add CSRF token
        },
        body: new URLSearchParams({
            post_id: postId,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error submitting report');
        }
        return response.json();
    })
    .then(data => {
        console.log('Report submitted successfully', data);

        // Mark the post as reported in the UI
        var postElement = document.getElementById('post' + postId);
        postElement.classList.add('reported');
    })
    .catch(error => {
        console.error('Error submitting report', error);
    });
}
