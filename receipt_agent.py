import os
from smolagents import LiteLLMModel, CodeAgent
import json
from tools import *

prompt_file_path = "system_prompt.txt"
contacts_file_path = "contacts.json"
receipt_file_path = "receipt.json"

import json

def load_system_prompt(prompt_file_path, contacts_file_path, receipt_file_path):
    # Load the system prompt from the text file
    with open(prompt_file_path, 'r') as prompt_file:
        system_prompt = prompt_file.read().strip()
    
    # Load the contact information from the JSON file
    with open(contacts_file_path, 'r') as contacts_file:
        contacts = json.load(contacts_file)
    
    # Format the contact information
    contact_info = "\n".join(
        [f"Name: {person['name']}, Number: {person['number']}" for person in contacts]
    )
    
    # Load the receipt information from the JSON file
    with open(receipt_file_path, 'r') as receipt_file:
        receipt = json.load(receipt_file)
    
    # Format the receipt information
    menu_items = "\n".join(
        [f"{item['name']}: ${item['cost']:.2f}" for item in receipt['menu_items']]
    )
    tip = f"Tip: ${receipt['tip']:.2f}"
    tax = f"Tax: ${receipt['tax']:.2f}"
    
    # Append the contact and receipt information to the system prompt
    full_prompt = (
        f"{system_prompt}\n\n"
        f"Here are the individuals' contact information:\n{contact_info}\n\n"
        f"Here is the receipt information:\n{menu_items}\n{tip}\n{tax}"
    )
    
    return full_prompt


def main():
    model = LiteLLMModel('openai/gpt-4o')
    task = load_system_prompt(prompt_file_path, contacts_file_path, receipt_file_path)
    agent = CodeAgent(tools=[send_message, wait_for_response], model=model, add_base_tools=False, max_steps=100)
    agent.run(task)

if __name__ == "__main__":
    main()
