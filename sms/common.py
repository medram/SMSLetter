import re
import csv
#import time
import requests

import vonage

from django.core.exceptions import ValidationError
from django_currentuser.middleware import get_current_user

from accounts.validators import moroccan_phone
from app import settings


def send_sms(contact, messages=None, subscription=None):

    if hasattr(messages, '__iter__'):
        # sending sms
        for message in messages:

            # check if the user have a valid subscription.
            if subscription is not None and subscription.amount <= 0:
                break

            # print(params)
            try:
                status = False
                if settings.VONAGE_KEY:
                    status = send_via_api_1(contact, message)
                elif settings.BULKSMS_TOKEN:
                    status = send_via_api_2(contact, message)

                # time.sleep(0.5)
                if status:
                    print('SMS sent successfully.')
                    subscription.amount -= 1
                    subscription.save()
            except Exception as e:
                print(e)


def phone_to_global_format(phone):
    return re.sub(r'^0', '212', phone)


def send_via_api_1(contact, message):
    client = vonage.Client(key=settings.VONAGE_KEY,
                           secret=settings.VONAGE_SECRET)
    sms = vonage.Sms(client)

    title = message.title if message.title else 'SMS'

    responseData = sms.send_message({
        "from": title,
        "to": phone_to_global_format(contact.phone),
        "text": message.message,
    })

    # print(responseData)

    if responseData["messages"][0]["status"] == "0":
        return True
    return False


def send_via_api_2(contact, message):
    URL = r'https://bulksms.ma/developer/sms/send'

    params = {
        'token': settings.BULKSMS_TOKEN,
        'tel': phone_to_global_format(contact.phone),
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

        # print('Message sent.')
        data = req.json()
        if data.get('success') == 1:
            return True
        return False
        # time.sleep(0.5)
    except Exception as e:
        return False


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
