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
