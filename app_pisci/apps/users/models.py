from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

class User(AbstractUser):
    email = models.EmailField(
        verbose_name= "Adresse e-mail",
        unique=True,
        validators=[EmailValidator(message="Adresse mail invalide")],
        error_messages={
            "unique": "Un utilisateur avec cet email existe déjà"
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
