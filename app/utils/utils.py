import uuid
from firebase_admin import credentials, messaging

def uuid4Str():
    test = str(uuid.uuid4())
    return test

def send_notification(title, message, token):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=message),
        token=token
    )
    messaging.send(message)