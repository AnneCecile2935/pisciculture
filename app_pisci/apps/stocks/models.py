from django.db import models
from apps.commun.models import TimeStampedModel
from apps.fournisseurs.models import Fournisseurs

class Aliment(TimeStampedModel):
    nom = models.CharField(max_length=100, verbose_name="Nom de l'alliment")
    description = models.TextField(verbose_name="Description")
    categorie = models.CharField(max_length=5, verbose_name="Type de l'aliment")
    fournisseur = models.ForeignKey(
        Fournisseurs,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Fournisseur"
    )

    def __str__(self):
        return f"{self.nom} ({self.fournisseur})" if self.fournisseur else self.nom

    class Meta:
        verbose_name = "Aliment"
        verbose_name_plural = "Aliments"
        ordering = ['categorie']
