from django.core.mail import send_mail
from django.conf import settings


def test_send_mail():
    try:
        send_mail(
            subject="Test Email",
            message="This is a test email from Django.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[
                "kinnelhead@gmail.com"
            ],  # Replace with the recipient's email
            fail_silently=False,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
