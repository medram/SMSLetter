from django import forms
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm

from .models import MyUser, MyGroup


admin.site.unregister(Group)


@admin.register(MyGroup)
class CustomGroupAdmin(GroupAdmin):
    pass


@admin.register(MyUser)
class CustomUserAdmin(UserAdmin):
    #add_form = UserCreationForm

    list_display = ('profile', 'email', 'full_name', 'get_gender', 'phone',
                    'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_display_links = ('email', 'full_name')
    # list_editable = ('is_active',)
    readonly_fields = ('profile_large', 'last_login',
                       'date_joined', 'updated', 'get_password')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('date_joined', 'is_staff', 'is_superuser',
                   'is_active', 'groups', 'gender')
    ordering = ('-date_joined',)
    # autocomplete_fields = ('',)

    fieldsets = (
        (None, {
            'fields': ('profile_large', 'profile_image')
        }),
        (_('Personal info'), {
            'fields': ('username', 'email', 'get_password', 'first_name', 'last_name', 'gender', 'phone', 'address')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined', 'updated')
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2')
        }),
    )

    def get_password(self, obj=None):
        return mark_safe("<a href='../password' class='btn btn-primary btn-sm text-white'><i class='fas fa-key fa-fw'></i> %s</a>" % _('Change Password'))
    get_password.short_description = 'Password'

    # def get_fieldsets(self, request, obj=None):
    #     # fieldsets = super().get_fieldsets(request, obj)
    #     return fieldsets

    def full_name(self, obj):
        full_name = obj.get_full_name()
        if full_name:
            return full_name
        return '-'

    def get_gender(self, obj=None):
        if obj.gender == obj.GENDER.MALE:
            return mark_safe(f'<i class="fas fa-fw fa-male text-primary"style="font-size: 1.2rem;"></i> {obj.get_gender_display()}')
        elif obj.gender == obj.GENDER.FEMALE:
            return mark_safe(f'<i class="fas fa-fw fa-female text-danger"style="font-size: 1.2rem;"></i> {obj.get_gender_display()}')
        else:
            return '-'
    get_gender.short_description = _('Gender')
    get_gender.admin_order_field = 'gender'

    # def save_model(self, request, obj, form, change):
    #     super(admin.ModelAdmin, self).save_model(request, obj, form, change)
