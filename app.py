import os
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from PIL import Image, ImageFilter  # For image processing
import openai  # For OpenAI API integration

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Directory to save uploaded images
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate_image", methods=["POST"])
def generate_image():
    """
    Generates an image using OpenAI's DALL-E API.
    """
    data = request.json
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response["data"][0]["url"]
        return jsonify({"image_url": image_url})
    except Exception as e:
        return jsonify({"error": f"Image generation failed: {str(e)}"}), 500


@app.route("/process_input", methods=["POST"])
def process_input():
    """
    Handles text input for natural language processing.
    """
    data = request.json
    user_input = data.get("input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        bot_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": f"Text processing failed: {str(e)}"}), 500


@app.route("/upload_image", methods=["POST"])
def upload_image():
    """
    Handles uploaded images for processing.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "No selected file"}), 400
    filename = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(filename)
    processed_path = apply_filter(filename)
    return jsonify({"image_url": processed_path})


def apply_filter(image_path):
    """
    Applies a simple filter to the uploaded image.
    """
    with Image.open(image_path) as img:
        processed_path = os.path.splitext(image_path)[0] + "_processed.jpg"
        img.filter(ImageFilter.CONTOUR).save(processed_path)
    return processed_path


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
