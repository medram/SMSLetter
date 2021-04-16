from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def moroccan_phone(value):
    if not ((len(value) == 10 and value.startswith('0')) or (len(value) == 12 and value.startswith('212'))):
        raise ValidationError(
            _('%(value)s is not a moroccan phone number!'), params={'value': value})
