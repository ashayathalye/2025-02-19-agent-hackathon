from twilio.rest import Client
from datetime import datetime, UTC
import time
import os

# Your Account SID and Auth Token from console.twilio.com
account_sid = "ACe5f30f9cde20df7c27bcc0f1218a9456"
auth_token  = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

# Get all messages
now = datetime.now(UTC)

while True:
    messages = client.messages.list(date_sent_after=now, to="+18449203535")
    now = datetime.now(UTC)

    # Print details for each message
    for message in messages:
        print(f"From: {message.from_}")
        print(f"To: {message.to}")
        print(f"Body: {message.body}")
        print(f"Date Sent: {message.date_sent}")
        print("-" * 50)

    time.sleep(1)
