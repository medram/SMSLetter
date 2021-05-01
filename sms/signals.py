import requests

from django.db.models.signals import post_save
from django.dispatch import receiver
from extra_settings.models import Setting

from .models import Contact


@receiver(post_save, sender=Contact)
def send_sms(sender, instance=None, created=False, **kwargs):
    if created and instance.send_sms:

        URL = r'https://bulksms.ma/developer/sms/send'
        user = instance.user
        messages = user.sms_list.all()  # get just the first message.

        # sending sms
        for message in messages:
            params = {
                'token': Setting.get('BULKSMS_TOKEN', default=''),
                'tel': instance.phone,
                'title': message.title,
                'shortcode': message.alias,
                'message': message.message,
                'attachement': message.attachement,
            }
            #print(params)
            try:
                req = requests.get(URL, params=params)

                print('Sending message...')
                print(req.json())
            except Exception as e:
                print(e)
