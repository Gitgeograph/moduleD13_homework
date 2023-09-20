from django.core.mail import send_mail

def send_notification_email(recipient, subject, message):
    from_email = 'Geographsawqa@yandex.ru'
    send_mail(subject, message, from_email, [recipient])