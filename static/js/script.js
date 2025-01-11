document.addEventListener("DOMContentLoaded", () => {
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const imageUploadButton = document.getElementById("image-upload-button");
    const imageInput = document.getElementById("image-input");
    const messages = document.getElementById("messages");

    // Enable Send Button
    userInput.addEventListener("input", () => {
        toggleSendButton();
    });

    imageInput.addEventListener("change", () => {
        toggleSendButton();
    });

    // Trigger hidden file input when image button is clicked
    imageUploadButton.addEventListener("click", () => {
        imageInput.click();
    });

    // Handle Send Button Click
    sendButton.addEventListener("click", () => {
        const message = userInput.value.trim();
        if (message) {
            addMessageToChat(message, "user-message"); // Display user's message
            if (message.toLowerCase().startsWith("generate:")) {
                const prompt = message.substring(9).trim();
                addWaitingEffect(); // Show waiting effect
                generateImage(prompt);
            } else {
                addWaitingEffect(); // Show waiting effect
                processText(message);
            }
        } else if (imageInput.files.length > 0) {
            addWaitingEffect(); // Show waiting effect
            uploadImage(imageInput.files[0]);
        }
        userInput.value = ""; // Clear input
        toggleSendButton();
    });

    // Handle Enter Key
    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && userInput.value.trim()) {
            event.preventDefault();
            sendButton.click();
        }
    });

    // Process Text Input
    function processText(input) {
        fetch("/process_input", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input }),
        })
            .then((response) => response.json())
            .then((data) => {
                removeWaitingEffect(); // Remove waiting effect
                if (data.response) {
                    addMessageToChat(data.response, "bot-message");
                } else if (data.error) {
                    addMessageToChat(`Error: ${data.error}`, "bot-message");
                }
            });
    }

    // Upload Image for Processing
    function uploadImage(file) {
        const formData = new FormData();
        formData.append("image", file);

        fetch("/upload_image", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                removeWaitingEffect(); // Remove waiting effect
                if (data.image_url) {
                    addImageToChat(data.image_url, "bot-message");
                } else {
                    addMessageToChat(`Error: ${data.error}`, "bot-message");
                }
            });
    }

    // Generate Image
    function generateImage(prompt) {
        fetch("/generate_image", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt }),
        })
            .then((response) => response.json())
            .then((data) => {
                removeWaitingEffect(); // Remove waiting effect
                if (data.image_url) {
                    addImageToChat(data.image_url, "bot-message");
                } else {
                    addMessageToChat(`Error: ${data.error}`, "bot-message");
                }
            });
    }

    // Add Message to Chat
    function addMessageToChat(content, type) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", type);
        messageElement.textContent = content;
        messages.appendChild(messageElement);
        messages.scrollTop = messages.scrollHeight;
    }

    // Add Image to Chat
    function addImageToChat(imageUrl, type) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", type);
        const img = document.createElement("img");
        img.src = imageUrl;
        img.alt = "Generated/Processed Image";
        img.style.maxWidth = "200px";
        img.style.borderRadius = "10px";
        messageElement.appendChild(img);
        messages.appendChild(messageElement);
        messages.scrollTop = messages.scrollHeight;
    }

    // Add Waiting Effect
    function addWaitingEffect() {
        const waitingElement = document.createElement("div");
        waitingElement.classList.add("message", "bot-message", "waiting");
        waitingElement.textContent = "Processing...";
        waitingElement.id = "waiting-effect"; // Add an ID for easy removal
        messages.appendChild(waitingElement);
        messages.scrollTop = messages.scrollHeight;
    }

    // Remove Waiting Effect
    function removeWaitingEffect() {
        const waitingElement = document.getElementById("waiting-effect");
        if (waitingElement) {
            waitingElement.remove();
        }
    }

    // Toggle Send Button State
    function toggleSendButton() {
        if (userInput.value.trim() || imageInput.files.length > 0) {
            sendButton.classList.add("enabled");
            sendButton.removeAttribute("disabled");
        } else {
            sendButton.classList.remove("enabled");
            sendButton.setAttribute("disabled", "true");
        }
    }
});