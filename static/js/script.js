document.addEventListener("DOMContentLoaded", () => {
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const messages = document.getElementById("messages");
    const socket = io();

    // Enable/Disable Send Button
    userInput.addEventListener("input", () => {
        if (userInput.value.trim()) {
            sendButton.classList.add("enabled");
            sendButton.removeAttribute("disabled");
        } else {
            sendButton.classList.remove("enabled");
            sendButton.setAttribute("disabled", "true");
        }
    });

    // Send Message
    sendButton.addEventListener("click", () => {
        const message = userInput.value.trim();
        if (!message) return;

        // Add User Message
        addMessage(message, "user-message");

        // Emit Message to Server
        socket.emit("send_message", { message });

        // Clear Input
        userInput.value = "";
        sendButton.classList.remove("enabled");
        sendButton.setAttribute("disabled", "true");
    });

    // Receive Bot Message
    socket.on("receive_message", (data) => {
        addMessage(data.message, "bot-message");
    });

    // Add Message to Chat
    function addMessage(content, type) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", type);
        messageElement.textContent = content;
        messages.appendChild(messageElement);
        messages.scrollTop = messages.scrollHeight; // Auto-scroll
    }
});
