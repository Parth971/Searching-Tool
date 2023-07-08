from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_forgot_password_email(user):
    token = PasswordResetTokenGenerator().make_token(user)
    link = F"{settings.FRONT_END_DOMAIN}/auth/restore-password/{user.id}/{token}/"

    context = {
        'subject': 'Restore Password',
        'uri': link,
    }
    send_mail(user.email, 'restore_password', context)


def send_email_verification_email(user):
    token = user.generate_activation_token()
    link = F"{settings.FRONT_END_DOMAIN}/auth/verify-email/{token}"
    context = {
        'subject': 'Email Verification',
        'uri': link,
    }
    send_mail(user.email, 'email_verification', context)


def send_mail(to, template, context):
    html_content = render_to_string(f'accounts/emails/{template}.html', context)
    msg = EmailMessage(context['subject'], html_content, to=[to])
    msg.send()


def upload_to(instance, filename):
    striped_email = instance.email.split("@")[0]
    extension = filename.split('.')[-1]
    return f'accounts/images/{striped_email}.{extension}'

