from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import integer_validator
from accounts.validators import moroccan_phone


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
