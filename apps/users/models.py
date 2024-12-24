"""
    Models for the custom user.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
        User in the system.
    """
    first_name = models.CharField(verbose_name=_('first name'), max_length=50)
    last_name = models.CharField(verbose_name=_('last name'), max_length=50)
    email = models.EmailField(verbose_name=_('email address'), db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)    
    groups = models.ManyToManyField('auth.Group', related_name='custom_users')
    role = models.CharField(max_length=20, choices=[
        ('instructor', _('Profesor')),
        ('student', _('Estudiante')),
    ], default='student')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_users')
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        return self.first_name


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification code for {self.user.email}"

    def is_valid(self):
      """
      Class to define the lifetime of the code
      """
      valid_period = timezone.now() - timezone.timedelta(minutes=10)
      return self.created_at >= valid_period
        
