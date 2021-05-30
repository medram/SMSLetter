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

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        contacts = Contact.objects.filter(
            user=user, phone=validated_data['phone'])
        if not contacts.count():
            contact = Contact.objects.create(**validated_data)
            # contact.user.add(user)
            return contact
        else:
            return contacts.all()[0]

    class Meta:
        model = Contact
        fields = ('id', 'name', 'phone', 'send_sms', 'created')
