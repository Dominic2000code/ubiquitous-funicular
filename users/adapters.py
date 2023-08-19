from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import build_absolute_uri
from django.core.mail import send_mail
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        email_subject = "Confirm Your Email"
        email_message = f"Your verification code is: {emailconfirmation.key}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = emailconfirmation.email_address.email

        # send mail asynchronously
        send_mail(email_subject, email_message, from_email,
                  [to_email], fail_silently=False)
