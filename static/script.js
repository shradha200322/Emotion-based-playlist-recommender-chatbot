// // document.addEventListener('DOMContentLoaded', () => {
// //     const chatbotIcon = document.querySelector('.chatbot-icon');
// //     const chatbotBox = document.getElementById('chatbot-box');
// //     const userInput = document.getElementById('user-input');
// //     const sendBtn = document.getElementById('send-btn');
// //     const chatMessages = document.getElementById('chat-messages');

// //     // Ensure elements exist
// //     if (!chatbotIcon || !chatbotBox || !userInput || !sendBtn || !chatMessages) {
// //         console.error("One or more chatbot elements are missing!");
// //         return;
// //     }

// //     // Toggle chatbot visibility
// //     chatbotIcon.addEventListener('click', () => {
// //         chatbotBox.style.display = chatbotBox.style.display === 'block' ? 'none' : 'block';
// //     });

// //     // Function to append messages to the chat
// //     const appendMessage = (message, isUser = false, isHtml = false) => {
// //         const messageDiv = document.createElement('div');
// //         if (isHtml) {
// //             messageDiv.innerHTML = message; // Render HTML content (for buttons)
// //         } else {
// //             messageDiv.textContent = message;
// //         }
// //         messageDiv.style.color = isUser ? '#007BFF' : '#555'; // User: Blue, Bot: Gray
// //         messageDiv.style.margin = '5px 0';
// //         chatMessages.appendChild(messageDiv);
// //         chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to latest message
// //     };

// //     // Function to send a message to the backend
// //     const sendMessage = async () => {
// //         const message = userInput.value.trim();
// //         if (!message) return;

// //         appendMessage(`You: ${message}`, true); // Show user message
// //         userInput.value = '';

// //         try {
// //             const response = await fetch('/predict', {  // Ensure the endpoint matches Flask
// //                 method: 'POST',
// //                 headers: { 'Content-Type': 'application/json' },
// //                 body: JSON.stringify({ message }),
// //             });

// //             if (!response.ok) throw new Error('Failed to get response from server');

// //             const data = await response.json();
// //             appendMessage(`Bot: ${data.emotion}`); // Append detected emotion

// //             // Create a button for the playlist link
// //             const buttonHtml = `
// //                 <a href="${data.playlist}" target="_blank" style="text-decoration: none;">
// //                     <button style="
// //                         background-color: #1DB954;
// //                         color: white;
// //                         padding: 8px 12px;
// //                         border: none;
// //                         border-radius: 5px;
// //                         cursor: pointer;
// //                         margin-top: 5px;
// //                     ">🎶 Listen on Spotify</button>
// //                 </a>`;
            
// //             appendMessage(buttonHtml, false, true); // Append the button as HTML
// //         } catch (error) {
// //             console.error('Error:', error);
// //             appendMessage('Bot: Sorry, something went wrong. Please try again later.');
// //         }
// //     };

// //     // Event listeners for sending messages
// //     sendBtn.addEventListener('click', sendMessage);
// //     userInput.addEventListener('keypress', (event) => {
// //         if (event.key === 'Enter') sendMessage();
// //     });
// // });
// document.addEventListener('DOMContentLoaded', () => {
//     const chatbotBox = document.getElementById('chatbot-box');
//     const userInput = document.getElementById('user-input');
//     const sendBtn = document.getElementById('send-btn');
//     const chatMessages = document.getElementById('chat-messages');
//     const discoverMoreBtn = document.querySelector('.button-container a'); // Select Discover More button

//     // Ensure elements exist
//     if (!chatbotBox || !userInput || !sendBtn || !chatMessages || !discoverMoreBtn) {
//         console.error("One or more chatbot elements are missing!");
//         return;
//     }

//     // Toggle chatbot visibility when clicking Discover More button
//     discoverMoreBtn.addEventListener('click', (event) => {
//         event.preventDefault(); // Prevent default anchor behavior
//         chatbotBox.style.display = chatbotBox.style.display === 'block' ? 'none' : 'block';
//     });

//     // Function to append messages to the chat
//     const appendMessage = (message, isUser = false, isHtml = false) => {
//         const messageDiv = document.createElement('div');
//         if (isHtml) {
//             messageDiv.innerHTML = message; // Render HTML content (for buttons)
//         } else {
//             messageDiv.textContent = message;
//         }
//         messageDiv.style.color = isUser ? '#007BFF' : '#555'; // User: Blue, Bot: Gray
//         messageDiv.style.margin = '5px 0';
//         chatMessages.appendChild(messageDiv);
//         chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to latest message
//     };

//     // Function to send a message to the backend
//     const sendMessage = async () => {
//         const message = userInput.value.trim();
//         if (!message) return;

//         appendMessage(`You: ${message}`, true); // Show user message
//         userInput.value = '';

//         try {
//             const response = await fetch('/predict', {  // Ensure the endpoint matches Flask
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ message }),
//             });

//             if (!response.ok) throw new Error('Failed to get response from server');

//             const data = await response.json();
//             appendMessage(`Bot: ${data.emotion}`); // Append detected emotion

//             // Create a button for the playlist link
//             const buttonHtml = `
//                 <a href="${data.playlist}" target="_blank" style="text-decoration: none;">
//                     <button style="
//                         background-color: #1DB954;
//                         color: white;
//                         padding: 8px 12px;
//                         border: none;
//                         border-radius: 5px;
//                         cursor: pointer;
//                         margin-top: 5px;
//                     ">🎶 Listen on Spotify</button>
//                 </a>`;
            
//             appendMessage(buttonHtml, false, true); // Append the button as HTML
//         } catch (error) {
//             console.error('Error:', error);
//             appendMessage('Bot: Sorry, something went wrong. Please try again later.');
//         }
//     };

//     // Event listeners for sending messages
//     sendBtn.addEventListener('click', sendMessage);
//     userInput.addEventListener('keypress', (event) => {
//         if (event.key === 'Enter') sendMessage();
//     });
// });


document.addEventListener('DOMContentLoaded', () => {
    const chatbotBox = document.getElementById('chatbot-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const discoverMoreBtn = document.querySelector('.button-container a');

    if (!chatbotBox || !userInput || !sendBtn || !chatMessages || !discoverMoreBtn) {
        console.error("One or more chatbot elements are missing!");
        return;
    }

    discoverMoreBtn.addEventListener('click', (event) => {
        event.preventDefault();
        chatbotBox.classList.toggle('show');
    });

    const appendMessage = (message, isUser = false, isHtml = false) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        if (isHtml) {
            messageDiv.innerHTML = message;
        } else {
            messageDiv.textContent = message;
        }
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(`You: ${message}`, true);
        userInput.value = '';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) throw new Error('Failed to get response from server');

            const data = await response.json();
            appendMessage(`Bot: ${data.emotion}`);

            const buttonHtml = `
                <a href="${data.playlist}" target="_blank" class="spotify-button">
                    🎶 Listen on Spotify
                </a>`;
            appendMessage(buttonHtml, false, true);
        } catch (error) {
            console.error('Error:', error);
            appendMessage('Bot: Sorry, something went wrong. Please try again later.');
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') sendMessage();
    });

    // Apply animations
    document.querySelectorAll('.user-message, .bot-message').forEach(msg => {
        msg.style.animation = isUser ? 'slideInRight 0.3s ease-out' : 'slideInLeft 0.3s ease-out';
    });
});
