# Install required packages
# pip install flask openai

import openai
import os
from flask import Flask, request, jsonify, session

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Add session configuration here
app.config['SECRET_KEY'] = '72e586d9ddc99caecbf8d3e9b69d18e3'  # Replace with the secure key you generated

# Flask's built-in session mechanism is used here without importing Flask-Session.

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spoke Medical Hearing Chat</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f5;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }

    #chat-container {
        width: 90%;
        max-width: 500px;
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        position: relative;
    }

    #chat-box {
        max-height: 500px;
        overflow-y: auto;
        padding-bottom: 50px;
    }

    /* Sticky Header Style */
    #sticky-header {
        position: sticky;  /* Makes the header stick to the top */
        top: 0;  /* Keeps it at the very top of the viewport */
        background-color: #007bff;  /* Blue background to distinguish it */
        color: #ffffff;  /* White text for better contrast */
        text-align: center;
        padding: 10px 20px;  /* Add some padding for breathing room */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);  /* Subtle shadow to make it pop out */
        z-index: 1000;  /* Keeps it above other elements */
    }

    /* Chat Container Styles */
    #chat-container {
        width: 90%;
        max-width: 500px;
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-top: 20px;  /* Ensure there's some spacing below the sticky header */
        position: relative;
    }

    /* Additional Styles for Better Consistency */
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f5;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 0;
    }

    /* Other existing styles (e.g., for messages, buttons, etc.) should remain here */

.message {
    display: flex;  /* Keeps the icon and message text aligned side by side */
    align-items: flex-start;  /* Aligns the icon to the top of the message content */
    padding: 15px;  /* Increased padding to ensure more space within the bubble */
    margin: 10px 0;
    border-radius: 10px;
}

.user-message {
    background-color: #0084ff;  /* Blue for user messages */
    color: #fff;
    text-align: left;  /* Properly aligns the message text */
    border-bottom-right-radius: 0;
    padding: 10px 15px;  /* Add padding to top, bottom, left, and right to make it evenly spaced */
    display: inline-block;  /* Keep message width only as wide as the content */
    max-width: 80%;  /* Restrict the width to make it look nicer on larger screens */
}

.bot-message {
    background-color: #f1f0f0;  /* Light gray for bot messages */
    color: #000;
    text-align: left;  /* Properly aligns the message text */
    border-bottom-left-radius: 0;
    padding: 10px 15px;  /* Add padding to top, bottom, left, and right to make it evenly spaced */
    display: inline-block;  /* Keep message width only as wide as the content */
    max-width: 80%;  /* Restrict the width to make it look nicer on larger screens */
}

.message i {
    font-size: 1.5em;  /* Size of the icon */
    margin-right: 10px;  /* Space between the icon and the text */
    color: #007bff;  /* Color for the icons */
    align-self: center;  /* Center the icon vertically within the message bubble */
}

.user-message i {
    color: #ffffff;  /* Icon color for user messages (white) */
}

.message-content {
    flex: 1;  /* Allow the content to use the remaining space */
}

.timestamp {
    color: white;  /* Set the timestamp color to white */
    font-size: 0.8em;  /* Reduce the font size slightly */
    opacity: 0.7;  /* Make it slightly transparent */
    display: block;  /* Ensure timestamp appears on a new line */
    margin-top: 5px;  /* Add space between the message text and timestamp */
}

    #user-input {
        width: calc(100% - 60px);
        padding: 10px;
        border-radius: 25px;
        border: 1px solid #ccc;
        outline: none;
        margin-right: 10px;
        box-sizing: border-box;
    }

    #send-button {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #0084ff;
        border: none;
        color: #fff;
        font-size: 18px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    #send-button:hover {
        background-color: #006bbd;
    }

    #suggested-questions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 10px;
    }

    .suggested-question {
        background-color: #e9ecef;
        color: #007bff;
        padding: 8px 12px;
        border-radius: 20px;
        cursor: pointer;
        border: none;
        transition: background-color 0.3s ease;
    }

    .suggested-question:hover {
        background-color: #d4d9de;
    }

    #welcome-message {
        font-size: 1em;
        color: #333;
        margin-bottom: 20px;
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }

    /* Typing Indicator Animation */
    .typing-indicator {
        display: flex;
        align-items: center;
        font-size: 1em;
        color: #888;  /* Light gray for "Our expert is typing..." */
    }

    .typing-indicator span {
        display: inline-block;
        width: 8px;
        height: 8px;
        margin: 0 2px;
        background-color: #888;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }

    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }

    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typing {
        0% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-5px);
        }
        100% {
            transform: translateY(0);
        }
    }
</style>
</head>
<body>
    <!-- Sticky Header with Welcome Message -->
    <div id="sticky-header">
        <h1>Spoke Medical Hearing Chat</h1>
        <p>Welcome to our new service that gives you personalized ear health guidance.</p>
    </div>

    <!-- Chat Container -->
    <div id="chat-container">
        <div id="chat-box"></div>

        <div id="user-input-container">
            <input type="text" id="user-input" placeholder="How can I help today? Please enter your question..." />
            <button id="send-button"><i class="fas fa-paper-plane"></i></button>
        </div>

        <div id="suggested-questions"></div>
    </div>
</body>

<script>
    $(document).ready(function () {
        // Function to append a message to the chat box
        function appendMessage(content, sender) {
            const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const messageClass = sender === 'user' ? 'user-message' : 'bot-message';

            // Choose the icon based on the sender
            const iconHTML = sender === 'user' ? 
                '<i class="fas fa-user-circle"></i>' : 
                '<i class="fas fa-stethoscope"></i>';

            // Add paragraph formatting for bot messages
            if (sender === 'bot') {
                // Assume sentences are separated by periods followed by a space, and convert to paragraph tags
                content = content.split('. ').map(sentence => `<p>${sentence.trim()}.</p>`).join("");
            }

            // Append the message with the appropriate icon
            $('#chat-box').append(
                `<div class="message ${messageClass}">
                    ${iconHTML}
                    <div class="message-content">${content}</div>
                    <span class="timestamp">${timestamp}</span>
                </div>`
            );
            $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
        }

        // This function handles the send operation for the message
        function sendMessage(userQuestion) {
            if (userQuestion !== "") {
                appendMessage(userQuestion, 'user');
                $('#user-input').val(''); // Clear the input field
                $('#suggested-questions').empty();

                // Add "Our expert is typing..." indicator with animation
                const typingIndicator = `
                    <div class="bot-message typing-indicator">
                        Our expert is typing
                        <span></span><span></span><span></span>  <!-- Animated dots -->
                    </div>`;
                $('#chat-box').append(typingIndicator);
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);

                console.log("Sending question to backend:", userQuestion); // Debugging log

                $.post('/ask', { question: userQuestion }, function (data) {
                    console.log("Response received from backend:", data); // Debugging log

                    // Remove "Our expert is typing..." indicator
                    $('.typing-indicator').remove();

                    if (data.response) {
                        appendMessage(data.response, 'bot');
                    } else {
                        appendMessage("Sorry, I didn't receive a valid response.", 'bot');
                    }

                    // If follow-up questions exist, generate suggested buttons
                    if (data.followUps && data.followUps.length > 0) {
                        generateSuggestedButtons(data.followUps);
                    }

                    // Change the input placeholder for follow-up questions
                    $('#user-input').attr("placeholder", "Please enter any follow-up question you may have...");
                }).fail(function () {
                    console.error("Error: Unable to connect to the backend service.");

                    // Remove "Our expert is typing..." indicator if request fails
                    $('.typing-indicator').remove();
                    
                    appendMessage("Sorry, there was an error processing your request. Please try again.", 'bot');
                });
            }
        }

        // This function generates suggested follow-up questions
        function generateSuggestedButtons(followUps) {
            $('#suggested-questions').empty();
            followUps.forEach(function (question) {
                $('#suggested-questions').append(
                    `<button class="suggested-question">${question}</button>`
                );
            });
        }

        // Event handler for clicking the send button
        $('#send-button').click(function () {
            const userQuestion = $('#user-input').val().trim();
            sendMessage(userQuestion);
        });

        // Event handler for pressing the Enter key
        $('#user-input').keypress(function (e) {
            if (e.which === 13) {
                const userQuestion = $('#user-input').val().trim();
                sendMessage(userQuestion);
            }
        });

        // Event handler for clicking suggested questions
        $('#suggested-questions').on('click', '.suggested-question', function () {
            const followUpQuestion = $(this).text();
            sendMessage(followUpQuestion);
        });
    });
</script>
</body>
</html>
    '''

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['question']

    # Debugging statement for user input
    print("User Input Received:", user_input)

    # Retrieve the conversation history from the session, or start a new one if it doesn't exist
    if 'conversation_history' not in session:
        session['conversation_history'] = []

    # Update conversation history with user input
    session['conversation_history'].append({"role": "user", "content": user_input})

    # Get the response from the chatbot, including follow-ups
    result = get_chatgpt_response(user_input, session['conversation_history'])
    
    # Extract the response text and follow-up suggestions from the result
    response_text = result.get('response', '')
    follow_ups = result.get('followUps', [])

    # Debugging statement for API response
    print("Response Text:", response_text)
    print("Follow-Ups to Provide:", follow_ups)

    # Update conversation history with the chatbot response as a string
    session['conversation_history'].append({"role": "assistant", "content": response_text})

    # Limit conversation history to avoid cookie overflow
    if len(session['conversation_history']) > 10:
        session['conversation_history'] = session['conversation_history'][-10:]

    # Save the updated conversation history back to the session
    session.modified = True

    # Return both the chatbot response and follow-up suggestions as JSON
    return jsonify({"response": response_text, "followUps": follow_ups})

def get_chatgpt_response(user_input, conversation_history):
    try:
        # Validate conversation history to ensure 'content' is always a string
        valid_conversation_history = []
        for entry in conversation_history:
            if isinstance(entry, dict) and "role" in entry and "content" in entry:
                if isinstance(entry["content"], str):
                    valid_conversation_history.append(entry)
                else:
                    # Log a warning for invalid content types
                    print("Warning: Skipping invalid content type in conversation history:", entry)

        # Combine system prompt, validated conversation history, and user input
        messages = [
            {"role": "system", "content": "You are a professional hearing health assistant. Provide detailed, informative answers that sound medical in nature, focusing on conditions related to hearing, including causes, symptoms, treatments, and prevention. Engage in follow-up questions, provide thorough explanations, and speak as though you are consulting a patient in a clinical setting."}
        ] + valid_conversation_history + [
            {"role": "user", "content": user_input}
        ]

        # Generate the response from the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )

        # Debugging output for generated response
        print("API Response Object:", response)

        # Extracting the response content
        response_text = response.choices[0].message['content']
        print("Generated Response Text:", response_text)

        # Define follow-up suggestions based on the user input
        follow_ups = []
        if "tinnitus" in user_input.lower():
            follow_ups = ["Should I see a doctor?", "What are the treatments for tinnitus?", "Can tinnitus be cured?"]
        elif "hearing loss" in user_input.lower():
            follow_ups = ["What are the common causes of hearing loss?", "Are there treatments for hearing loss?", "Should I consider a hearing test?"]
        elif "ear infection" in user_input.lower():
            follow_ups = ["How can I treat an ear infection?", "Is an ear infection serious?", "Can ear infections cause hearing problems?"]

        # Debugging output for follow-up suggestions
        print("Follow-Up Suggestions:", follow_ups)

        return {"response": response_text, "followUps": follow_ups}

    except Exception as e:
        # If there's an error, print the error and return a structured response
        print("Error occurred in get_chatgpt_response:", str(e))
        return {"response": "I'm sorry, an error occurred while processing your request.", "followUps": []}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
