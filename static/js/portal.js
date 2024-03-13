// Check if the user is logged in
function checkLoginStatus() {
    // Assume a function isLoggedIn() is defined elsewhere that checks if the user is logged in
    // Replace isLoggedIn() with the actual function that checks if the user is logged in
    if (isLoggedIn()) {
        // User is logged in, replace the placeholder with the actual username
        document.querySelector('.profile-session .username').textContent = 'John Doe'; // Replace 'John Doe' with the actual username
    } else {
        // User is not logged in, show the login button
        document.querySelector('.profile-session .login-signup').style.display = 'inline';
    }
}

// Call the function to check the login status when the page loads
window.onload = function() {
    checkLoginStatus();
};

// Click event listener for the analyze button
document.getElementById('analyzeBtn').addEventListener('click', function() {
    var review = document.getElementById('review').value;
    var rating = document.querySelector('input[name="rating"]:checked');

    if (review.trim() === '') {
        alert('Please write a review.');
        return;
    }

    if (!rating) {
        alert('Please rate your experience.');
        return;
    }

    var sentiment = analyzeSentiment(review);
    var ratingValue = rating.value;

    document.getElementById('result').innerHTML = `
        <p>Sentiment: ${sentiment}</p>
        <p>Rating: ${ratingValue} stars</p>
    `;
});

// Function to analyze sentiment
function analyzeSentiment(review) {
    // Simple sentiment analysis function, you can replace it with your own implementation
    // For demonstration purpose, just returning 'Positive' if the review contains the word 'good'
    if (review.toLowerCase().includes('good')) {
        return 'Positive';
    } else {
        return 'Negative';
    }
}
