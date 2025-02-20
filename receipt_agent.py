import os
from smolagents import LiteLLMModel, CodeAgent, tool
from pydantic import BaseModel
import json

prompt_file_path = "system_prompt.txt"
contacts_file_path = "contacts.json"
receipt_file_path = "receipt.json"

def multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

@tool
def send_message(number: str, message: str) -> None:
    """
    Send a text message to a given phone number.

    Args:
        number: The phone number to send the message to.
        message: The message to send. The message should be at most 140 characters.
    """
    print(f"[tool execution] Sending message to {number}: {message}")

class Message(BaseModel):
    from_number: str
    message: str    

@tool
def wait_for_response() -> Message:
    """
    Waits until a text message is received from someone. This function returns _any_ message that is received, not just the one from any particular person you are waiting for. You need to look at the sender's number to figure out who has sent the message.

    Returns:
        A message object containing the sender's number and the message content.
    """
    print("[tool execution] Waiting for response...")
    number = input("Enter the number of the sender: ")
    message = multiline_input("Enter the message content (end with an empty line): ")
    return Message(from_number=number, message=message)

class Person(BaseModel):
    name: str
    number: str

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
