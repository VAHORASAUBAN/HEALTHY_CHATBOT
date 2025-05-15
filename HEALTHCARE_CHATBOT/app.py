from flask import Flask, render_template, request, jsonify
import google.generativeai as ai

app = Flask(__name__)

# Replace with a secure way to store API keys, such as environment variables, for production use
API_KEY = 'AIzaSyAmfUktmBJJ5juTDZCP1_ULPeu2dWl7LEo'

ai.configure(api_key=API_KEY)

# model = ai.GenerativeModel("gemini-1.5-flash")
model = ai.GenerativeModel("gemini-1.5-flash-8b")

class AI_Assistant:
    def __init__(self):
        # Initialize AI model with psychiatrist persona
        self.full_transcript = [
            {"role": "system", "content": "You are a compassionate and responsible psychiatrist. Listen attentively, provide supportive responses, and offer guidance in a calm, reassuring tone."},
        ]
        self.chat = model.start_chat()

    def generate_ai_response(self, user_input):
        # Append user message to conversation context
        self.full_transcript.append({"role": "user", "content": user_input})

        # Generate a medium-length response with the Gemini API
        prompt = f"As a psychiatrist, provide a supportive, medium-length response (around 2-3 sentences) to: {user_input}"
        response = self.chat.send_message(prompt)
        ai_response = response.text.strip()

        # Append AI response to conversation context
        self.full_transcript.append({"role": "assistant", "content": ai_response})
        return ai_response

ai_assistant = AI_Assistant()

# Default route
@app.route('/')
def index():
    return render_template('chatbot.html')

# API route for chatbot responses
@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        user_message = request.json.get("message")  # Get message from user
        print("User:", user_message)  # Debugging

        if not user_message:
            return jsonify({"response": "Error: No message received"}), 400  # Return error if empty

        # Generate AI response
        if user_message.lower() == "bye":
            response_text = "Goodbye! Take care of yourself."
        else:
            response_text = ai_assistant.generate_ai_response(user_message)

        print("AI:", response_text)  # Debugging
        return jsonify({"response": response_text})  # Send JSON response

    except Exception as e:
        print("Error:", str(e))  # Print error in terminal
        return jsonify({"response": "Internal Server Error"}), 500  # Return proper error

if __name__ == '__main__':
    app.run(debug=True)
