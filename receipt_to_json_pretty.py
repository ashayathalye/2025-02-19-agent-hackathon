import openai
import os
import argparse
import base64

# Retrieve OpenAI API key from environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not client.api_key:
    raise ValueError("Missing OpenAI API key. Set it as an environment variable: OPENAI_API_KEY")

def encode_image(image_path):
    """Encodes an image as a Base64 data URL for OpenAI API."""
    with open(image_path, "rb") as image_file:
        return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

def extract_receipt_data(image_path):
    """Extracts receipt data from an image using GPT-4o and prints the JSON output."""
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

    extracted_text = response.choices[0].message.content.strip()
    print(extracted_text)  # Output the formatted JSON directly

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract receipt data from an image using GPT-4o.")
    parser.add_argument("image_path", type=str, help="Path to the receipt image (PNG format).")
    extract_receipt_data(parser.parse_args().image_path)