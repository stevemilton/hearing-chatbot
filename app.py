# Install required packages
# pip install flask openai

import openai
import os

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hearing Chatbot</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    </head>
    <body>
        <h1>Hearing Health Chatbot</h1>
        <div>
            <textarea id="userQuestion" rows="4" cols="50" placeholder="Ask your question about hearing..."></textarea>
            <br>
            <button id="askButton">Ask</button>
        </div>
        <div id="responseBox">
            <h3>Response:</h3>
            <p id="botResponse"></p>
        </div>

        <script>
            $(document).ready(function() {
                $('#askButton').click(function() {
                    const userQuestion = $('#userQuestion').val();
                    $.post('/ask', { question: userQuestion }, function(data) {
                        $('#botResponse').text(data.response);
                    });
                });
            });
        </script>
    </body>
    </html>
    '''

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['question']
    response = get_chatgpt_response(user_input)
    return jsonify({"response": response})

def get_chatgpt_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for answering questions about hearing issues."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message['content']
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
