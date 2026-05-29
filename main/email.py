from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from gallery2 import settings


def send_letter(name, email, message):
    subject = f'Новое сообщение от {name}'
    message = render_to_string('email/letter.html', {
        'name': name,
        'email': email,
        'subject': subject,
        'message': message,
    })
    msg = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.EMAIL_ADMIN])
    msg.content_subtype = 'html'
    msg.send(fail_silently=False)