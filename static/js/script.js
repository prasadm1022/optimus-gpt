document.addEventListener("DOMContentLoaded", () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const socket = io(); // Connect to the Socket.IO server

    // Check if there is any text typed and enable/disable the button
    userInput.addEventListener('input', () => {
        if (userInput.value.trim() === '') {
            sendButton.classList.remove('enabled');
            sendButton.setAttribute('disabled', 'true');
        } else {
            sendButton.classList.add('enabled');
            sendButton.removeAttribute('disabled');
        }
    });

    // Handle sending the message when the button is clicked
    sendButton.addEventListener('click', () => {
        if (userInput.value.trim()) {
            const message = userInput.value.trim();
            // Emit the message to the server using Socket.IO
            socket.emit('send_message', { message });

            // Add user message to the chat
            addMessageToChat(message, 'user-message');

            userInput.value = ''; // Clear input after sending
            sendButton.classList.remove('enabled');
            sendButton.setAttribute('disabled', 'true');
        }
    });

    // Listen for the bot's response from the server
    socket.on('receive_message', (data) => {
        const botMessage = data.message;
        addMessageToChat(botMessage, 'bot-message');
    });

    // Function to add message to the chat
    function addMessageToChat(message, messageType) {
        const chatBox = document.getElementById('chat-box');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', messageType);
        messageElement.innerHTML = `<div class="message-text">${message}</div>`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    }
});