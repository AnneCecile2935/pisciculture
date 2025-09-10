from django.db import models

class TimeStampedModel(models.Model):
    """
    Classe de base abstraite pour ajouter automatiquement :
    - date_creation : date/heure de création
    - date_modification : date/heure de dernière modification
    """
    date_creation = models.DateTimeField(
        verbose_name="Date de création",
        auto_now_add=True  # Rempli automatiquement à la création
    )
    date_modification = models.DateTimeField(
        verbose_name="Date de modification",
        auto_now=True  # Mis à jour automatiquement à chaque modification
    )

    class Meta:
        abstract = True  # Indique que cette classe ne crée pas de table en base
