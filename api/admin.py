from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy

admin.site.unregister(TokenProxy)
