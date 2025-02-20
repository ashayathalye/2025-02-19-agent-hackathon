from pydantic import BaseModel
from smolagents import tool
import os
from twilio.rest import Client
from datetime import datetime, UTC
import time

TWILIO_ACCOUNT_SID = "ACe5f30f9cde20df7c27bcc0f1218a9456"
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = "+18449203535"
SEND_LIMIT = 30

if TWILIO_AUTH_TOKEN:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    client = None

def multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

sent_messages = 0

@tool
def send_message(number: str, message: str) -> None:
    """
    Send a text message to a given phone number.

    Args:
        number: The phone number to send the message to.
        message: The message to send. The message should be at most 140 characters.
    """
    if client:
        if sent_messages >= SEND_LIMIT:
            raise Exception("too many messages")
        msg = client.messages.create(to=number, from_=TWILIO_PHONE_NUMBER, body=message)
        print(f"[tool execution] Message sent to {number}: {msg.sid}")
    else:
        print(f"[tool execution] Sending message to {number}: {message}")

class Message(BaseModel):
    from_number: str
    message: str    

now = datetime.now(UTC)

message_index = 0

@tool
def wait_for_response() -> Message:
    """
    Waits until a text message is received from someone. This function returns _any_ message that is received, not just the one from any particular person you are waiting for. You need to look at the sender's number to figure out who has sent the message.

    Returns:
        A message object containing the sender's number and the message content.
    """
    global message_index
    if client:
        messages = client.messages.list(date_sent_after=now, to=TWILIO_PHONE_NUMBER)
        while not (message_index < len(messages)):
            messages = client.messages.list(date_sent_after=now, to=TWILIO_PHONE_NUMBER)
            time.sleep(1)
        msg = messages[-1-message_index]
        message_index += 1
        m = Message(from_number=msg.from_, message=msg.body)
        print(f"[tool execution] Returning message from {m.from_number}: {m.message}")
        return m
    else:
        print("[tool execution] Waiting for response...")
        number = input("Enter the number of the sender: ")
        message = multiline_input("Enter the message content (end with an empty line): ")
        return Message(from_number=number, message=message)
