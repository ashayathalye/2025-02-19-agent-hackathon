import openai
import os
import base64
import json

# Retrieve OpenAI API key from environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not client.api_key:
    raise ValueError("Missing OpenAI API key. Set it as an environment variable: OPENAI_API_KEY")

def encode_image(image_path):
    """Encodes an image as a Base64 data URL for OpenAI API."""
    with open(image_path, "rb") as image_file:
        return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

def clean_json_response(response_text):
    """Cleans the JSON output by removing markdown formatting if present."""
    if response_text.startswith("```json"):
        response_text = response_text[7:-4]  # Remove ```json\n at the start and \n``` at the end
    return json.loads(response_text)  # Ensure it's valid JSON

def receipt2json(image_path):
    """Extracts receipt data from an image using GPT-4o and returns a JSON string."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Extract the receipt data into the following JSON format:\n\n"
                            "{\n"
                            "    \"menu_items\": [\n"
                            "        {\n"
                            "            \"name\": \"Margherita Pizza\",\n"
                            "            \"cost\": 12.99\n"
                            "        },\n"
                            "        {\n"
                            "            \"name\": \"Caesar Salad\",\n"
                            "            \"cost\": 8.50\n"
                            "        }\n"
                            "    ],\n"
                            "    \"tip\": 10.00,\n"
                            "    \"tax\": 5.00\n"
                            "}\n\n"
                            "Use this format exactly but replace the sample data with the correct values from the receipt."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": encode_image(image_path)}
                    }
                ]
            }
        ],
        max_tokens=500
    )

    st = response.choices[0].message.content.strip()  # Return extracted JSON as a string
    si = st.find('{')
    ei = st.rfind('}')
    return json.loads(st[si:ei+1])
