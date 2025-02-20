from pydantic import BaseModel
from smolagents import tool

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
