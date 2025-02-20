import json

def clean_json_response(response_text):
    """Cleans the JSON output by removing markdown formatting if present."""
    if response_text.startswith("```json"):
        response_text = response_text[7:-4]  # Remove ```json\n at the start and \n``` at the end
    return json.loads(response_text)  # Ensure it's valid JSON

def receipt2json(image_path):
    """Extracts receipt data from an image using GPT-4o and returns a JSON object."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the receipt data into valid JSON format as shown below:\n"
                                             "{\n"
                                             "    \"menu_items\": [\n"
                                             "        {\n"
                                             "            \"name\": \"Margherita Pizza\",\n"
                                             "            \"cost\": 12.99\n"
                                             "        }\n"
                                             "    ],\n"
                                             "    \"tip\": 10.00,\n"
                                             "    \"tax\": 5.00\n"
                                             "}"},
                    {"type": "image_url", "image_url": {"url": encode_image(image_path)}}
                ]
            }
        ],
        max_tokens=500
    )

    extracted_text = response.choices[0].message.content.strip()
    return clean_json_response(extracted_text)  # Ensure valid JSON is returned