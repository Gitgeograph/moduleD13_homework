from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver 
from .models import Comment
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from .utils import send_notification_email

@receiver(post_save, sender=Comment)
def notify_about_Comment(sender, instance, created, **kwargs):
    if created:
        user = instance.commentPost.author
        post = instance.commentPost
        html = render_to_string(
            template_name='mail/new_comment.html',
            context={
                'comment': instance,
                'user': user.name,
                'post': post,
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'New comment notification',
            body="",
            from_email='Geographsawqa@yandex.ru',
            to=[user.name.email],
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()


# @receiver(post_save, sender=Comment)
# def notify_about_accept_Comment(sender, instance, created, **kwargs):
#     if not created and instance.is_accepted :
#         user = instance.commentUser
#         html = render_to_string(
#             template_name='mail/comment_accept.html',
#             context={
#                 'comment': instance,
#                 'user': user,
#             }
#         )

#         msg = EmailMultiAlternatives(
#             subject=f'New comment notification',
#             body="",
#             from_email='Geographsawqa@yandex.ru',
#             to=[user.email],
#         )

#         msg.attach_alternative(html, 'text/html')
#         msg.send()
#         instance.accepted_notification_sent = True
#         instance.save()
