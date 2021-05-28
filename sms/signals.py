from django.db.models.signals import post_save
from django.dispatch import receiver
from extra_settings.models import Setting

from .models import Contact
from .common import send_sms


@receiver(post_save, sender=Contact)
def send_sms_message(sender, instance=None, created=False, **kwargs):
    if created and instance.send_sms:
        user = instance.user
        messages = user.sms_list.all()  # get just the first message.
        send_sms(instance, messages)
