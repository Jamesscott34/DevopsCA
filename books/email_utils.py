from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user):
    subject = "Welcome to Book Catalog!"
    message = f"Hi {user.username}, welcome to the Book Catalog App."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


def send_custom_email(to_email, subject, message):
    """
    Send a custom email to the specified recipient.
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])

