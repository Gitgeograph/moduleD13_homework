from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from datetime import timedelta
from django.utils import timezone
from board.models import Post, Author


def weekly_notification():
    date = timezone.now() - timedelta(weeks=1)
    users_set = set()
    post_week = list(Post.objects.filter(created_at__gte = date).order_by('-created_at')) 
    for post in Post.objects.all():
        users_set.add(Author.objects.get(name = post.author.name))
    for user in users_set:                                 
        html = render_to_string(
            template_name='mail/weekly_notification.html',
            context={
                'posts_week': post_week,
                'user': user
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Weekly Posts',
            body="",
            from_email='Geographsawqa@yandex.ru',
            to=[user.name.email],
        )

        msg.attach_alternative(html, 'text/html')
        msg.send()