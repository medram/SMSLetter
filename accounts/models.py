import os
import secrets
from PIL import Image

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, Group, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail

from . import validators


def _user_profile_path(instance, filename):
    return f"profiles/{secrets.token_hex(16)}.png"


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        email = str(email).lower()
        if not email:
            raise ValueError('Users must have a email')

        user = self.model(email=self.normalize_email(email), username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password):
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        max_length=256,
        unique=True,
        error_messages={
            'unique': _('A user with that email address already exists.'),
        },
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    username = models.CharField(_('Username'), max_length=150)

    class GENDER(models.IntegerChoices):
        MALE = (1, _('Male'))
        FEMALE = (2, _('Female'))

    profile_image = models.ImageField(
        upload_to=_user_profile_path, default="profiles/default.jpg", blank=True
    )

    first_name = models.CharField(
        _('First name'), max_length=32, null=True, blank=True)
    last_name = models.CharField(
        _('Last name'), max_length=32, null=True, blank=True)

    gender = models.IntegerField(choices=GENDER.choices, default=GENDER.MALE)
    phone = models.CharField(max_length=10, blank=True,
                             null=True, validators=[validators.moroccan_phone])

    # status = models.IntegerField(choices=Status.choices, default=Status.APPROVED)
    address = models.CharField(max_length=256, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # def clean(self):
    #     super().clean()
    #     self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name:
            return self.first_name
        return self.last_name

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):
        # set the token if not exists.
        # if not self.token:
        #     token = secrets.token_hex(32)
        #     try:
        #         while Profile.objects.get(token=token):
        #             token = secrets.token_hex(32)
        #     except Profile.DoesNotExist:
        #         pass
        #     self.token = token

        # getting the old profile images.
        old_user = None
        try:
            old_user = type(self).objects.get(email=self.email)
        except type(self).DoesNotExist:
            pass

        # Try set the default avatar
        if self.profile_image.name == '':
            self.profile_image.name = 'profiles/default.jpg'

        # save profile
        super().save(*args, **kwargs)

        # resize profile image.
        size = (200, 200)
        try:
            if (
                    self.profile_image.name
                    and self.profile_image.name != old_user.profile_image.name
            ):
                try:
                    image = Image.open(self.profile_image.path)
                    # image.thumbnail(size)
                    image = image.resize(size)
                    image.save(self.profile_image.path, "PNG")
                except IOError:
                    pass
                else:
                    # removing old profile image.
                    try:
                        if old_user.profile_image.name != 'profiles/default.jpg':
                            os.remove(old_user.profile_image.path)
                    except IOError:
                        pass
        except:
            pass

    def __str__(self):
        return self.email


class MyGroup(Group):
    class Meta:
        verbose_name = 'Group'
