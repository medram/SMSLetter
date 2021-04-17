from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import integer_validator


class Contact(models.Model):
    name = models.CharField(
        _('Contact name'), max_length=32, null=True, blank=True)
    phone = models.CharField(
        _('Phone number'),
        max_length=10,
        validators=[integer_validator],
        help_text=_('e.g. 06xxxxxxxx'))

    created = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(get_user_model(), related_name='contacts')

    def __str__(self):
        return self.phone


class SMS(models.Model):
    message = models.TextField(_('Message'), max_length=160, help_text=_('maximum characters: 160'))
    user = models.ForeignKey(
        get_user_model(), related_name='sms_list', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'SMS'
        verbose_name_plural = 'SMS List'

    def __str__(self):
        return self.message
