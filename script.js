// Select the "Start Conversation" button
const startConversationButton = document.querySelector('.primary');

// Add event listener for click event
startConversationButton.addEventListener('click', () => {
    // Apply fade-out class to the body
    document.body.classList.add('fade-out');

    // Wait for the fade-out animation to complete before navigating
    setTimeout(() => {
        window.location.href = 'dashboard.html'; // Redirect to assistant page
    }, 500); // Duration of the fade-out effect (same as the transition time in CSS)
});
