from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string
from django.conf import settings
from django.dispatch import receiver
from .models import Post, Subscription, PostCategory

def send(preview, pk, title, subscribers_emails):
    html_content = render_to_string(
        'sb/post_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/NEWS/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.SITE_URL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers_emails = []

        for x in categories:
            subscribers = Subscription.objects.filter(category=x)
            subscribers_emails += [subs.user.email for subs in subscribers]

        send(instance.preview(), instance.pk, instance.title, subscribers_emails)
