from django.contrib import admin

# admin.site.site_title = f'{settings.APP_NAME}'
# admin.site.site_header = f'{settings.APP_NAME}'


class MyAdminSite(admin.AdminSite):
    index_title = 'Dashboard'
    enable_nav_sidebar = False
