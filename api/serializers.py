from rest_framework import serializers
from django.contrib.auth import get_user_model

from sms.models import Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email',
                  'profile_image', 'first_name', 'last_name', 'phone', 'date_joined')
        read_only_fields = ('profile_image', 'date_joined')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'phone', 'created')
