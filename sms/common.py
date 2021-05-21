import csv
#import time
import requests

from django.core.exceptions import ValidationError
from django_currentuser.middleware import get_current_user
from extra_settings.models import Setting

from accounts.validators import moroccan_phone


def send_sms(contact, messages=None):
    URL = r'https://bulksms.ma/developer/sms/send'

    if hasattr(messages, '__iter__'):
        # sending sms
        for message in messages:
            params = {
                'token': Setting.get('BULKSMS_TOKEN', default=''),
                'tel': contact.phone,
                'message': message.message
            }
            if message.title:
                params.setdefault('title', message.title)

            if message.alias:
                params.setdefault('shortcode', message.alias)

            if message.attachement:
                params.setdefault('attachement', message.attachement)

            # print(params)
            try:
                req = requests.get(URL, params=params)

                print('Message sent.')
                print(req.json())
                # time.sleep(0.5)
            except Exception as e:
                print(e)


def generate_contact_list(contact_list):
    from .models import Contact

    contacts = set()

    if bool(contact_list.file):
        # creating contacts from a CSV file.
        with open(contact_list.file.path) as f:
            reader = csv.DictReader(f)
            for line in reader:
                try:
                    moroccan_phone(line['phone'])
                except ValidationError:
                    pass
                else:
                    name = line.get('name')
                    phone = line.get('phone')
                    current_user = get_current_user()

                    contact = Contact.objects.create(
                        name=name, phone=phone, user=current_user)
                    contacts.add(contact)  # add to the Set

    # adding users contacts
    for user in contact_list.users.all():
        contacts.update(user.contacts.all())

    # adding more selected contacts.
    contacts.update(contact_list.contacts.all())

    # asign all selected contacts to this list.
    contact_list.contacts.add(*contacts)
