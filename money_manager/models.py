import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=150)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.category_name


@receiver(post_save, sender=User)
def create_category_for_user(sender, instance, created, **kwargs):
    list_of_default_categories = [
        "Забота о себе", "Зарплата", "Здоровье и фитнес",
        "Кафе и рестораны", "Машина", "Образование",
        "Отдых и развлечения", "Платежи, комиссии", "Покупки: одежда, техника",
        "Продукты", "Проезд"
    ]
    if created:
        for category in list_of_default_categories:
            Category.objects.create(user=instance, category_name=category)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_of_transaction = models.IntegerField(default=0)
    date_of_transaction = models.DateField('date_of_transaction',
                                           default=timezone.localtime(timezone.now()).date())
    time_of_transaction = models.TimeField('time_of_transaction',
                                           default=timezone.localtime(timezone.now()).time().strftime('%H:%M'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    organisation = models.CharField(blank=False, max_length=50)
    comment = models.TextField(blank=True, max_length=500)


class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_category_for_user(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(user=instance)
