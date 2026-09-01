from accounts.tasks import send_otp_email

def send_otp_email_task(user, otp):
    # pass serialized user email string to the celery task
    send_otp_email.delay(user.email, otp, user.username)