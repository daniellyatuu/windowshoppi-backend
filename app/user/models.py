from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import Group
from app.master_data.models import Category
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

###########################################################################
# extend User model .start
###########################################################################


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('username is required')
        if not password:
            raise ValueError('password is required')

        user = self.model(username=username)
        user.set_password(password)  # change user password
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):

        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, blank=True, null=True)
    superuser = models.BooleanField(default=False)  # super user
    staff = models.BooleanField(default=False)  # staff user non superuser
    active = models.BooleanField(default=True)  # can login
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'  # username field
    REQUIRED_FIELDS = []  # Username & Password are required by default.

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_active(self):
        return self.active

    def call_phone_number(self):
        user_contact = self.phone_numbers.all()[0]
        return user_contact.call

    def whatsapp_phone_number(self):
        user_contact = self.phone_numbers.all()[0]
        return user_contact.whatsapp

    class Meta:
        ordering = ['-id']

###########################################################################
# extend User model ./end
###########################################################################


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Contact(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    user = models.ForeignKey(
        User, related_name="phone_numbers", on_delete=models.CASCADE)
    call = models.CharField(validators=[phone_regex], max_length=17)
    whatsapp = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s : %s' % (self.user, self.call)


class UserLocation(models.Model):
    user = models.ForeignKey(
        User, related_name='user_locations', on_delete=models.CASCADE)
    location_name = models.CharField(max_length=255)
    lattitude = models.FloatField()
    longitude = models.FloatField()
    date_retrieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location_name

    class Meta:
        ordering = ['-id']
