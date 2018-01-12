from twilio.rest import Client
import messages


def send_message(Number,mail):
    client = Client(messages.account_sid, messages.auth_token)
    message = client.messages.create(
        to=Number,                                     # "+919876543210"
        from_=messages.Twilio_Number,
        body=messages.message)
    print("message successfully sent,:",message)

