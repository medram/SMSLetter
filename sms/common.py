import csv

from django.core.exceptions import ValidationError
from django_currentuser.middleware import get_current_user
from accounts.validators import moroccan_phone


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
