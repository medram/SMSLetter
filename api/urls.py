from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from django.urls import path, include
from django.conf import settings

from . import views

app_name = __package__

urlpatterns = [
    #path('user/', views.UserDetail.as_view()),
    #path('auth/', views.obtain_auth_token),
    path('auth/', views.CustomAuthToken.as_view()),
    path('contact/', views.ContactList.as_view()),
    path('contact/<int:pk>', views.ContactDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
