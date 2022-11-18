# Generated by Django 4.1.3 on 2022-11-15 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('money_manager', '0017_alter_transaction_time_of_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='time_of_transaction',
            field=models.TimeField(default='14:05', verbose_name='time_of_transaction'),
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]