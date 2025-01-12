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

import openai
import os

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_openai_image(prompt):
    """
    Generates an image using OpenAI's DALL-E API.
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response["data"][0]["url"]
        return {"image_url": image_url}
    except Exception as e:
        return {"error": f"Image generation failed: {str(e)}"}


def process_openai_text(user_input):
    """
    Processes text input using OpenAI's GPT API.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        bot_response = response["choices"][0]["message"]["content"]
        return {"response": bot_response}
    except Exception as e:
        return {"error": f"Text processing failed: {str(e)}"}
