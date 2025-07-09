import random
from twilio.rest import Client
import os
from dotenv import load_dotenv
from django.contrib.auth.hashers import make_password

def generate_and_send_otp(phone_number):
    load_dotenv()
    otp = random.randint(int(os.getenv('a')), int(os.getenv('b')))
    # Use a service like Twilio to send the OTP via SMS
    account_sid = os.getenv('account_sid')
    auth_token = os.getenv('auth_token')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=os.getenv('twilio_phone'),  # Your Twilio phone number
        to=phone_number
    )
    return otp

