import os
from smolagents import LiteLLMModel, CodeAgent, tool
from pydantic import BaseModel

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

def load_system_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def main():
    model = LiteLLMModel('openai/gpt-4o')
    customer = Person(name="John Doe", number="1234567890")
    ceo = Person(name="Jane Smith", number="0987654321")
    task = load_system_prompt('system_prompt.txt').format(
        customer_name=customer.name, 
        customer_number=customer.number, 
        ceo_name=ceo.name, 
        ceo_number=ceo.number
    )
    agent = CodeAgent(tools=[send_message, wait_for_response], model=model, add_base_tools=False, max_steps=100)
    agent.run(task)

if __name__ == "__main__":
    main()
