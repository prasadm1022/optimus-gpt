# Copyright 2025 Prasad Madusanka Basnayaka
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from PIL import Image, ImageFilter  # For image processing
from models.openai import generate_openai_image, process_openai_text  # Importing OpenAI helpers

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

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

    result = generate_openai_image(prompt)
    if "image_url" in result:
        return jsonify({"image_url": result["image_url"]})
    return jsonify({"error": result["error"]}), 500


@app.route("/process_input", methods=["POST"])
def process_input():
    """
    Handles text input for natural language processing.
    """
    data = request.json
    user_input = data.get("input")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    result = process_openai_text(user_input)
    if "response" in result:
        return jsonify({"response": result["response"]})
    return jsonify({"error": result["error"]}), 500


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
