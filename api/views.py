from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import permissions, mixins, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from sms.models import Contact
from .serializers import ContactSerializer, UserSerializer


class ContactViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class ProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user

    def list(self, request, pk=None):
        return Response(self.get_serializer(request.user).data)


# class CustomAuthToken(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user']
#         user_serialiser = UserSerializer(user)
#         token, created = Token.objects.get_or_create(user=user)
#         result = {'token': token.key}
#         result.update(user_serialiser.data)

#         return Response(result)
