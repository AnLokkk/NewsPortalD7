import datetime
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Post, Subscription
from django.conf import settings


@shared_task
def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week).order_by('-dateCreation')
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers_emails = []
    for x in categories:
        subscribers = Subscription.objects.filter(category__name=x)
        subscribers_emails += [subs.user.email for subs in subscribers]
    subscribers_emails = set(subscribers_emails)

    html = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='всё новое за неделю',
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html, 'text/html')
    msg.send()