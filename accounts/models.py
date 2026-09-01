from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
import uuid
# from django import User

from accounts.manager import CustomUserManager

from django.utils import timezone

# Create your models here.
ROLE_CHOICES = (
    ('customer', 'Customer'),
    ('admin', 'Admin'),
    ('VENDOR', 'Vendor'),
)

class User(AbstractUser, PermissionsMixin):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  username = models.CharField(max_length=150, unique=True)
  email = models.EmailField(unique=True)
  phone_number = models.CharField(max_length=20, blank=True, null=True)
  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
  is_active = models.BooleanField(default=True)
  is_verified = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  date_joined = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  last_login = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return self.email

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']

class ProfilePicture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_picture')
    image = models.ImageField(upload_to='profile_pictures/', default='user_profile/default.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile Picture"


class OTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    hash_otp = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        # OTP is valid for 10 minutes
        expiration_time = self.created_at + timezone.timedelta(minutes=10)
        return timezone.now() > expiration_time

    def __str__(self):
        return f"{self.user.email}'s OTP"