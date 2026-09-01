from random import randint
from ..models import OTP
# hashing
from django.contrib.auth.hashers import make_password, check_password

from accounts.utils.emails import send_otp_email_task

def generate_send_otp(user):
    # generate random 6 digit number
    otp = randint(100000, 999999)

    # hash the otp before saving to database (for security reasons)
    hashed_otp = make_password(str(otp))

    # Save the hashed OTP to the database
    OTP.objects.create(user=user, hash_otp=hashed_otp)

    # Send the OTP to the user's email asychronously using Celery
    send_otp_email_task(user, otp)

def verify_otp(user, otp):
    try:
        otp_record = OTP.objects.filter(user=user).latest('created_at')
        if otp_record.is_expired():
            otp_record.delete()  # Clean up expired OTP
            return False
        
    except OTP.DoesNotExist:
        return False
    # Check if the provided OTP matches the hashed OTP in the database
    if check_password(str(otp), otp_record.hash_otp):
        # If OTP is valid, delete the OTP record from the database
        otp_record.delete()
        return True