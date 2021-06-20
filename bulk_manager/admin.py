from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from background_task.models import Task, CompletedTask
from django.utils.html import mark_safe

from .models import Campaign

# unregister Background_task app
admin.site.unregister(Task)
admin.site.unregister(CompletedTask)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'run_at',
                           'repeat', 'repeat_until', 'contact_lists', 'messages')}),
        (_('Access Info'), {
         'fields': ('created_by_profile_large', 'created', 'updated')})
    )
    list_display = ('id', 'title', 'total_messages', 'total_contacts', 'get_status',
                    'created_by_profile', 'created')
    list_display_links = ('id', 'title')
    filter_horizontal = ('contact_lists', 'messages')
    readonly_fields = ('updated', 'created', 'updated_by',
                       'created_by', 'updated_by_profile', 'created_by_profile', 'created_by_profile_large')
    list_filter = ('created', 'status', 'created_by')
    search_fields = ('id', 'title')
    date_hierarchy = 'created'
    radio_fields = {'repeat': admin.VERTICAL}
    actions = ('stop_campaign',)

    def total_messages(self, obj=None):
        return obj.messages.count()

    def total_contacts(self, obj=None):
        return sum([l.contacts.count() for l in obj.contact_lists.all()])

    def get_status(self, obj=None):
        css_class = ''
        if obj.status == obj.Status.READY:
            css_class = 'badge-secondary'
        elif obj.status == obj.Status.SENDING:
            css_class = 'badge-primary'
        elif obj.status == obj.Status.COMPLETED:
            css_class = 'badge-success'
        elif obj.status == obj.Status.STOPPED:
            css_class = 'badge-warning'

        return mark_safe(f"<span class='badge badge-pill {css_class}'>{obj.get_status_display().upper()}</span>")

    def stop_campaign(self, request, queryset):
        for campaign in queryset.all():
            if campaign.status != Campaign.Status.COMPLETED:
                campaign.status = Campaign.Status.STOPPED
                campaign.save()
        self.message_user(request, _('Stopped successfully.'))
    stop_campaign.short_description = _('Stop campaign')
