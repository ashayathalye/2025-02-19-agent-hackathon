from twilio.rest import Client

# Your Account SID and Auth Token from console.twilio.com
account_sid = "ACe5f30f9cde20df7c27bcc0f1218a9456"
auth_token  = "3cc60dfed9491123275140d2837e6139"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+15088166033",
    from_="+18449203535",
    body="Hello from Python!")

print(message.sid)