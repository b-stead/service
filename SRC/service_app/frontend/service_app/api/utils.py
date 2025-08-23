from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from smtplib import SMTPException
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .tokens import BlacklistableAccessToken

User = get_user_model()
        
def send_activation_email(user):
    """
    Placeholder function to simulate sending an activation email.
    In a real application, this function would send an email to the user
    with a link to activate their account.
    """
    if user.email is None:
        return False
    
    oauth_token = AccessToken.for_user(user)
    link = settings.BASE_URL + reverse('activate', kwargs={'token': str(oauth_token)})
    
    try:
        send_mail(
            subject='Activate your account',
            message=f'Please click the link to activate your account: {link}',
            from_email=settings.EMAIL_HOST_USER,  # Correct placement of from_email
            recipient_list=[user.email],
            fail_silently=False,
        )
    except SMTPException as e:
        print(f"Failed to send email: {e}")
        return False
    print(f"Activation email sent to {user.email}")
    return True

def get_user_from_token(token):
    """
    Retrieve the user associated with the given token.
    """
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)

        sub = access_token.get('sub')
        print(f"User sub from token: {sub}")
        if not sub:
            raise Exception("Token does not contain a subject")
        return user
    except User.DoesNotExist:
        print("User not found for the provided token.")
        return ValidationError("User not found for the provided token.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    
def revoke_token(token):
    """
    Revoke the given token by blacklisting it.
    """
    access_token = BlacklistableAccessToken(token)
    access_token.blacklist()

def is_token_valid(token):
    """
    Check if the provided token is valid.
    """
    access_token = BlacklistableAccessToken(token)

    try:
        access_token.check_exp()
        access_token.check_blacklist()
        return True
    except TokenError as e:
        print(f"Token error: {e}")
        return False