# Generated by Django 3.2 on 2021-05-01 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0006_auto_20210429_0248'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='send_sms',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Send SMS messages now'),
        ),
    ]
