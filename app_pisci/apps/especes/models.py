from django.db import models
from apps.commun.models import TimeStampedModel

class Espece(TimeStampedModel):
    nom_commun = models.CharField(
        max_length=100,
        verbose_name="Nom commun",
        help_text="Ex: Truite Arc en ciel"
    )
    nom_scientifique = models.CharField(
        max_length=100,
        verbose_name='Nom scientifique',
        help_text="Ex: Oncorhynchus mykiss"
        )
    est_actif = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Cocher si cette espèce est acutellement élevée"
    )

    class Meta:
        verbose_name = "Espèce"
        verbose_plural = "Espèces"
        ordering = ['nom_commun']
        permissions = [
            ("view_espece", "Can view espèce"),
            ("add_espece", "Can add espèce"),
            ("change_espece", "Can change espèce"),
            ("delete_espece", "Can delete espèce"),
        ]

    def __str__(self):
        return f"{self.nom_commun} ({self.nom_scientifique})"
