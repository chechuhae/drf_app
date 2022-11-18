from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from money_manager.models import Category


@shared_task
def send_mail_task():
    print("Mail sending")
    for user in User.objects.all():
        subject = 'Your daily statistic'
        categories = Category.objects.filter(user=user.id)
        context = {'categories': categories, 'user': user}
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, render_to_string('money_manager/statistic.html', context), email_from, recipient_list)
        print('mail was sent to {0}'.format(user.username))
    return 'Mail successfully send to all users'
