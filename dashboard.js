document.querySelector('.send-button').addEventListener('click', function() {
    const inputField = document.querySelector('.chat-input');
    const messageText = inputField.value;

    if (messageText.trim() !== "") {
        const messageBox = document.querySelector('.chat-box');
        const newMessage = document.createElement('div');
        newMessage.classList.add('message', 'sent');
        newMessage.innerHTML = `<p>${messageText}</p>`;
        messageBox.appendChild(newMessage);
        inputField.value = "";
        messageBox.scrollTop = messageBox.scrollHeight;
    }
});

document.querySelector('.chat-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.querySelector('.send-button').click();
    }
});
// Add this script to dashboard.js


