import os

from dotenv import load_dotenv

from twilio.rest import Client

load_dotenv()

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
client = Client(account_sid, auth_token)


def send_sms(to, number):
    message = client.messages \
                    .create(
                         body=f"Your confirmation number is {number}",
                         from_='+13473345196',
                         to=to
                     )

    return message.status
