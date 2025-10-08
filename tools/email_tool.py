# tools/email_tool.py
import os
import smtplib
import ssl
import random
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_otp_email(receiver_email: str) -> str:
    """Generates a 6-digit OTP and sends it to the user's email."""

    # Generate a random 6-digit OTP
    otp = str(random.randint(100000, 999999))

    message = f"""\
Subject: Your OTP for YES Ai

Welcome to YES Ai

Your One-Time Password (OTP) for verifying your account is: {otp}
This OTP is valid for 10 minutes.
Do not share the OTP with anyone to avoid misuse of your account.


This is an auto-generated email. Please do not reply to this email.

Regards,
YES Ai Team
"""

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, message)

        # Shudhu OTP-ta return kora hocche jate amra pore verify korte pari
        return otp

    except Exception as e:
        print(f"Failed to send email: {e}")
        return "Failed to send OTP"