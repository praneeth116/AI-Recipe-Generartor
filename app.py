from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# URL for the Rasa REST endpoint
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/')
def index():
    # Serve the chat interface
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Receive JSON payload from the client
    data = request.get_json()
    sender = data.get("sender", "default")
    message = data.get("message")
    
    if not message:
        return jsonify({"error": "No message provided."}), 400

    # Create payload for Rasa
    payload = {
        "sender": sender,
        "message": message
    }
    
    try:
        # Forward the message to Rasa REST endpoint
        response = requests.post(RASA_URL, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
    except requests.RequestException as e:
        return jsonify({"error": "Failed to get response from Rasa.", "details": str(e)}), 500

    # Return Rasa's response (expected to be a list of messages)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=5000, debug=True)
