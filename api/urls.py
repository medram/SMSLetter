#from rest_framework.urlpatterns import format_suffix_patterns
#from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from django.conf import settings

from . import views

app_name = __package__


router = routers.DefaultRouter(trailing_slash=True)
router.register(r'contact', views.ContactViewSet)
router.register(r'profile', views.ProfileViewSet)

urlpatterns = [
    #path('auth/', views.CustomAuthToken.as_view()),
    path('auth/', obtain_auth_token),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
