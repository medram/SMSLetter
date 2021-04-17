from rest_framework.urlpatterns import format_suffix_patterns
#from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from rest_framework import routers
from django.urls import path, include
from django.conf import settings

from . import views

app_name = __package__

router = routers.SimpleRouter(trailing_slash=True)
router.register(r'contact', views.ContactViewSet)

urlpatterns = [
    path('auth/login/', views.CustomAuthToken.as_view()),
    path('', include(router.urls)),
]


# urlpatterns = [
#     path('auth/', views.CustomAuthToken.as_view()),
#     path('contact/', views.ContactList.as_view()),
#     path('contact/<int:pk>', views.ContactDetail.as_view()),
# 	  path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)