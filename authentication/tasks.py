from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_activation_email(username, email, token):
    subject = "Verify Your Email for E-Commerce API"
    activation_link = f"http://127.0.0.1:8000/activate/{token}"
    # Plain text version (optional fallback)
    message = f"""
    Hi {username},

    Thank you for signing up for our E-Commerce platform! 
    Click the link below to verify your email:

    {activation_link}

    This link will expire in 24 hours.
    """

    # HTML version (formatted with clickable link)
    html_message = f"""
    <p>Hi {username},</p>
    <p>Thank you for signing up for our E-Commerce platform! Click the button below to verify your email:</p>
    <p><a href="{activation_link}" style="color: #1a73e8; text-decoration: none; ">
        Click here to verify your email
    </a></p>
    <p>This link will expire in <strong>24 hours</strong>.</p>
    <p>If the button above doesn’t work, copy and paste this URL into your browser:</p>
    <p><a href="{activation_link}">{activation_link}</a></p>
    <p>Best regards,<br><strong>The E-Commerce Team</strong><br>support@yourdomain.com</p>
    """
    send_mail(
        subject,
        message,  # Plain text version
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
        html_message=html_message  # HTML version for rich text emails
    )
    return "Mail sent"
