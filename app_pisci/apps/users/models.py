from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class User(AbstractUser):
    email = models.EmailField(
        verbose_name= "Adresse e-mail",
        unique=True,
        blank=False,
        null=False,
        validators=[EmailValidator(message="Adresse mail invalide")],
        error_messages={
            "unique": "Un utilisateur avec cet email existe déjà",
            "blank": "L'adresse email est obligatoire",
        }
    )

    username = models.CharField(
        verbose_name= "Nom d'utilisateur",
        max_length=50,
        unique=True,
        error_messages={"unique": "Ce nom d'utilisateur est déjà pris.",
        }
    )

    is_admin = models.BooleanField(
        verbose_name= "Est Administrateur",
        default=False
    )

    def save(self, *args, **kwargs):
        if not self.email:
            raise ValidationError({"email": "L'adresse email est obligatoire"})
        # Force is_staff à True si is_superuser est True
        if self.is_superuser:
            self.is_staff = True
        # Synchronise is_staff avec is_admin
        if self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'users'

    def __str__(self):
        return self.email

