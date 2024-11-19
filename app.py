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
        <title>Hearing Health Chatbot</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                color: #333;
                text-align: center;
                margin: 0;
                padding: 0;
            }
            #chatContainer {
                max-width: 600px;
                margin: 50px auto;
                background: #ffffff;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                position: relative;
            }
            h1 {
                color: #007bff;
            }
            #responseBox {
                margin-top: 20px;
                text-align: left;
                max-height: 400px;
                overflow-y: auto;
                padding-right: 10px;
            }
            #botResponse {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .user-message, .bot-message {
                padding: 10px;
                border-radius: 15px;
                width: fit-content;
                max-width: 70%;
                margin-bottom: 10px;
                position: relative;
            }
            .user-message {
                background-color: #007bff;
                color: #fff;
                align-self: flex-end;
            }
            .bot-message {
                background-color: #f1f0f0;
                color: #333;
                align-self: flex-start;
            }
            .timestamp {
                font-size: 0.8em;
                color: #888;
                position: absolute;
                bottom: -18px;
                right: 10px;
            }
            #typingIndicator {
                font-style: italic;
                color: #888;
                display: none;
                margin-top: 10px;
            }
            #followUpSection {
                margin-top: 20px;
            }
            #userQuestion {
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            #askButton {
                margin-top: 10px;
                padding: 10px 20px;
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s ease, transform 0.1s ease;
            }
            #askButton:hover {
                background-color: #0056b3;
                transform: scale(1.05);
            }
            #suggestedQuestions {
                margin-top: 15px;
            }
            .suggested-button {
                padding: 8px 15px;
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                margin: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .suggested-button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div id="chatContainer">
            <h1>Hearing Health Chatbot</h1>
            <div id="responseBox">
                <h3>Response:</h3>
                <div id="botResponse"></div>
                <div id="typingIndicator">Bot is typing...</div>
            </div>
            <div id="suggestedQuestions"></div>
            <div id="followUpSection">
                <textarea id="userQuestion" rows="4" placeholder="How can I help today? Please enter your question..."></textarea>
                <br>
                <button id="askButton"><i class="fas fa-paper-plane"></i> Ask</button>
            </div>
        </div>

        <script>
            $(document).ready(function() {
                // When the user clicks the "Ask" button
                $('#askButton').click(function() {
                    const userQuestion = $('#userQuestion').val().trim();
                    if (userQuestion !== "") {
                        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                        // Append user message with timestamp
                        $('#botResponse').append("<div class='user-message'>" + userQuestion + "<span class='timestamp'>" + timestamp + "</span></div>");
                        $('#userQuestion').val("");
                        $('#userQuestion').attr("placeholder", "Please enter any follow-up question you may have");

                        // Show typing indicator only after user input is valid
                        $('#typingIndicator').show();

                        // Send the user's question to the server
                        $.post('/ask', { question: userQuestion }, function(data) {
                            // Hide typing indicator
                            $('#typingIndicator').hide();

                            // Append bot message with paragraph structure and timestamp
                            const botResponse = "<div class='bot-message'>" + data.response.replace(/\\n/g, '<br><br>') + "<span class='timestamp'>" + timestamp + "</span></div>";
                            $('#botResponse').append(botResponse);

                            // Add suggested follow-up buttons if available
                            generateSuggestedButtons(data.followUps);

                            // Scroll to the bottom of the responseBox to keep latest message in view
                            $('#responseBox').animate({ scrollTop: $('#responseBox').prop("scrollHeight")}, 500);
                        });
                    }
                });

                // When the user clicks a suggested follow-up button
                $(document).on('click', '.suggested-button', function() {
                    const suggestedQuestion = $(this).text();
                    $('#userQuestion').val(suggestedQuestion);
                    $('#askButton').click();
                });

                // Function to generate suggested follow-up buttons
                function generateSuggestedButtons(followUps) {
                    $('#suggestedQuestions').empty();
                    if (followUps && followUps.length > 0) {
                        followUps.forEach(function(question) {
                            const button = "<button class='suggested-button'>" + question + "</button>";
                            $('#suggestedQuestions').append(button);
                        });
                    }
                }
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
