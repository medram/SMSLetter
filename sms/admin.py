from django.contrib import admin

from .models import SMS, Contact, ContactList


@admin.register(Contact)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'created')
    ordering = ('-created',)
    search_fields = ('name', 'phone', 'user__email', 'user__phone')
    list_filter = ('created', 'user')
    autocomplete_fields = ('user',)


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'alias', 'message', 'user', 'created')
    list_display_links = ('id', 'message', 'title', 'alias')
    search_fields = ('message',)
    list_filter = ('created', 'user')
    ordering = ('-created',)

    autocomplete_fields = ('user',)


@admin.register(ContactList)
class ContactListAdmin(admin.ModelAdmin):
    list_display = ('list_name', 'get_total_contacts',
                    'created_by', 'updated_by', 'created')
    list_filter = ('created',)
    exclude = ('created_by',)
    filter_horizontal = ('contacts', 'users')

    def has_change_permission(self, req, obj=None):
        return False

    def get_total_contacts(self, obj=None):
        return obj.contacts.count()

    get_total_contacts.short_description = 'Total Contacts'
