from django.contrib import admin
from .models import SMS, Contact


@admin.register(Contact)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'created')
    ordering = ('-created',)
    search_fields = ('name', 'phone', 'user__email', 'user__phone')
    list_filter = ('created', 'user')
    autocomplete_fields = ('user',)


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    list_display = ('message', 'created')
    search_fields = ('message',)
    list_filter = ('created', 'user')
    ordering = ('-created',)

    autocomplete_fields = ('user',)
