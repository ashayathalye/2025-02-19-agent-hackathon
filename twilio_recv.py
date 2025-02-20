from twilio.rest import Client
from datetime import datetime, UTC
import time

# Your Account SID and Auth Token from console.twilio.com
account_sid = "ACe5f30f9cde20df7c27bcc0f1218a9456"
auth_token  = "3cc60dfed9491123275140d2837e6139"

client = Client(account_sid, auth_token)

# Get all messages
now = datetime.now(UTC)

while True:
    messages = client.messages.list(date_sent_after=now, to="+18449203535")

    # Print details for each message
    for message in messages:
        print(f"From: {message.from_}")
        print(f"To: {message.to}")
        print(f"Body: {message.body}")
        print(f"Date Sent: {message.date_sent}")
        print("-" * 50)

    time.sleep(1)

    now = datetime.now(UTC)