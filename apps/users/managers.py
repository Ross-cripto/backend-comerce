"""
  Module to manning a User Custom Model
"""

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
  """
    Custom Object Manager
  """
  def email_validator(self, email):
    """
    Validate email Function.
    """
    try:
      validate_email(email)
      return True
    except ValidationError:
      raise ValueError(_("Debe proveer un correo valido. "))
    
  def create_user(self, first_name, last_name, email, password, **extra_fields):
        """
        Create, save and return a new user.
        """
        
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
            if self.model.objects.filter(email=email).exists():
                raise ValueError(_("Ya existe una cuenta con esta dirección de Correo. "))
        else:
            raise ValueError(_("Usuarios deben tener un email."))

        user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self.db)
        return user

  def create_superuser(self, first_name, last_name, email, password, **extra_fields):
      """
      Create, save and return a new superuser.
      """

      extra_fields.setdefault("is_staff", True)
      extra_fields.setdefault("is_superuser", True)
      extra_fields.setdefault("is_active", True)  # Asegúrate de que is_active esté en True

      if extra_fields.get("is_staff") is not True:
          raise ValueError(_("The superuser must be staff"))

      if extra_fields.get("is_superuser") is not True:
          raise ValueError(_("The superuser must have superuser=True"))

      if not password:
          raise ValueError(_("Superuser needs a password"))

      if email:
          email = self.normalize_email(email)
          self.email_validator(email)
          if self.model.objects.filter(email=email).exists():
              raise ValueError(_("Email address already in use."))
      else:
          raise ValueError(_("Superuser must have an email address."))

      # Aquí es donde se pasan correctamente los extra_fields que incluyen is_staff e is_superuser
      user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
      user.set_password(password)
      user.save(using=self._db)
      return user
