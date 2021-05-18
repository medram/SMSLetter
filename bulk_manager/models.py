from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from background_task.models import Task, CompletedTask
from django_currentuser.db.models import CurrentUserField

from sms.models import ContactList


class Campaign(models.Model):
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
