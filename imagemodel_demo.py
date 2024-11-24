import os
import base64
import openai
from dotenv import load_dotenv
load_dotenv()

# Encode the image in Base64
image_path = "dummy.jpg"  # Ensure the image format matches the "image/jpeg" MIME type
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

# Prepare the request body
request_body = {
    "model": "Llama-3.2-11B-Vision-Instruct",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                {"type": "text", "text": "Summarize"},
            ],
        }
    ],
    "max_tokens": 300,  # Optional, adjust as needed
    "temperature": 0.0,  # Optional, adjust as needed
    "top_p": 0.1,  # Optional, adjust as needed
    "top_k": 50,  # Optional, adjust as needed
    "stop": ["<eot>"],  # Optional
}

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),  # Ensure the API key is set as an environment variable
    base_url="https://api.sambanova.ai/v1",
)

# Send the request
response = client.chat.completions.create(
    model=request_body["model"],
    messages=request_body["messages"],
    max_tokens=request_body["max_tokens"],
    temperature=request_body["temperature"],
    top_p=request_body["top_p"],
    stop=request_body["stop"],
)

# Print the response
print(response.choices[0].message.content)
