from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from background_task.models import Task, CompletedTask
from django_currentuser.db.models import CurrentUserField

from sms.models import ContactList, SMS


class Campaign(models.Model):

    class Status(models.IntegerChoices):
        SENDING = (0, _('Sending'))
        COMPLETED = (1, _('Completed'))
        READY = (2, _('Ready'))
        STOPPED = (3, _('Stopped'))

    title = models.CharField(_('Campaign name'), max_length=256, unique=True)
    run_at = Task._meta.get_field('run_at')
    repeat = Task._meta.get_field('repeat')
    repeat_until = Task._meta.get_field('repeat_until')
    task = models.OneToOneField(
        Task, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    completed_task = models.OneToOneField(
        CompletedTask, null=True, blank=True, default=None, on_delete=models.SET_NULL)

    contact_lists = models.ManyToManyField(
        ContactList, verbose_name=_('Contact Lists'), blank=True)

    messages = models.ManyToManyField(SMS, verbose_name=_(
        'Select SMS'), help_text=_('Select SMS messages to send.'), blank=True)

    status = models.IntegerField(choices=Status.choices, default=Status.READY)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    updated_by = CurrentUserField(
        related_name='campaign_updated_by', on_update=True)
    created_by = CurrentUserField(related_name='campaign_created_by')

    class Meta:
        ordering = ('-created',)

    @admin.display(description=_('Created By'))
    def created_by_profile(self):
        return self.created_by.profile_with_info(size=32)

    @admin.display(description=_('Created By'))
    def created_by_profile_large(self):
        return self.created_by.profile_with_info()

    @admin.display(description=_('Updated By'))
    def updated_by_profile(self):
        return self.updated_by.profile_with_info(size=32)

    def reload(self):
        new_obj = self.__class__.objects.get(pk=self.pk)
        self.__dict__.update(new_obj.__dict__)
