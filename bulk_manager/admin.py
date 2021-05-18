from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Campaign


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'run_at',
                           'repeat', 'repeat_until', 'contact_lists')}),
        (_('Access Info'), {'fields': ('created_by_profile_large', 'created', 'updated')})
    )
    list_display = ('id', 'title', 'created_by_profile', 'created')
    list_display_links = ('id', 'title')
    filter_horizontal = ('contact_lists',)
    readonly_fields = ('updated', 'created', 'updated_by',
                       'created_by', 'updated_by_profile', 'created_by_profile', 'created_by_profile_large')
    list_filter = ('created', 'created_by')
    search_fields = ('id', 'title')
    date_hierarchy = 'created'
    radio_fields = {'repeat': admin.VERTICAL}
