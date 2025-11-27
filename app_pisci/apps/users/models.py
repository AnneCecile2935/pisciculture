from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class User(AbstractUser):
    """
    Modèle personnalisé pour les utilisateurs de l'application.
    Hérite de AbstractUser pour bénéficier des fonctionnalités de base de Django (authentification, permissions, etc.).
    Ajoute des champs spécifiques comme `is_admin` et impose des validations strictes sur l'email et le nom d'utilisateur.
    """
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

    is_staff = models.BooleanField(
        verbose_name="Est membre du staff",
        default=False,
    )

    def save(self, *args, **kwargs):
        """
        Sauvegarde l'utilisateur après validation des données.
        Vérifie que l'email est renseigné et synchronise `is_staff` avec `is_admin` ou `is_superuser`.

        Raises:
            ValidationError: Si l'email n'est pas fourni.
        """
        if not self.email:
            raise ValidationError({"email": "L'adresse email est obligatoire"})
        # Synchronise is_staff avec is_admin ou is_superuser
        self.is_staff = self.is_admin or self.is_superuser
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta:
        - app_label (str): Nom de l'application Django à laquelle ce modèle appartient.
        """
        app_label = 'users'

    def __str__(self):
        """
        Retourne l'adresse email de l'utilisateur comme représentation lisible.

        Returns:
            str: Adresse email de l'utilisateur.
        """
        return self.email

