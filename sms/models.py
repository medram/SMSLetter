from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import integer_validator
from accounts.validators import moroccan_phone
from django_currentuser.db.models import CurrentUserField

from . import common

User = get_user_model()


class Contact(models.Model):
    name = models.CharField(
        _('Contact name'), max_length=32, null=True, blank=True)
    phone = models.CharField(
        _('Phone number'),
        max_length=10,
        validators=[integer_validator, moroccan_phone],
        help_text=_('e.g. 06xxxxxxxx'))

    created = models.DateTimeField(auto_now_add=True)
    #user = models.ManyToManyField(get_user_model(), related_name='contacts')
    user = models.ForeignKey(
        get_user_model(), related_name='contacts', on_delete=models.CASCADE)

    send_sms = models.BooleanField(
        _('Send SMS messages now'), default=False, null=True, blank=True)

    def __str__(self):
        return self.phone


class SMS(models.Model):
    title = models.CharField(_('Title'), max_length=32, null=True, blank=True)
    alias = models.CharField(_('Alias'), max_length=11, null=True,
                             blank=True, help_text=_('alpha-numériques (a-z,A-Z,0-9)'))
    attachement = models.CharField(
        _('Attachement (URL)'), max_length=100, null=True, blank=True)

    message = models.TextField(
        _('Message'), max_length=450, help_text=_('maximum characters: 459'))
    user = models.ForeignKey(
        get_user_model(), related_name='sms_list', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'SMS'
        verbose_name_plural = 'SMS List'

    def __str__(self):
        return f'Message id: #{self.id}'


def get_temp_path(instance, filename):
    return f'tmp/tmp_{filename}'


class ContactList(models.Model):
    list_name = models.CharField(max_length=32, unique=True)
    file = models.FileField(
        _('CSV file'), upload_to=get_temp_path, null=True, blank=True, help_text=_('Upload Contacts from a CSV file'))
    users = models.ManyToManyField(
        User, related_name='contact_lists', blank=True, verbose_name=_('Select from Users Contacts'))

    contacts = models.ManyToManyField(
        'Contact', related_name='contact_lists', blank=True, verbose_name=_('Select more Contacts'))

    updated_by = CurrentUserField(related_name='updated_by', on_update=True)
    created_by = CurrentUserField(related_name='created_by')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'List'
        verbose_name_plural = 'Lists'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.list_name} ({self.contacts.count()})'

    def save(self, *args, **kwargs):
        # need to create contacts and asign it to this list.
        if self.is_created:
            transaction.on_commit(
                lambda: common.generate_contact_list(self))

        super().save(*args, **kwargs)

    @property
    def is_created(self):
        return False if self.pk else True
