from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from models.openai import get_openai_response

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    bot_message = get_openai_response(user_message)
    return jsonify({"response": bot_message})


@socketio.on('send_message')
def handle_send_message(message):
    user_message = message.get("message")
    if user_message:
        bot_message = get_openai_response(user_message)
        emit('receive_message', {'message': bot_message})


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
