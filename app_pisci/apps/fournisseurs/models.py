from django.db import models
from apps.commun.models import TimeStampedModel

class Fournisseurs(TimeStampedModel):
    nom = models.CharField(max_length=100, verbose_name="Nom du fournisseur")
    adresse = models.TextField(verbose_name="Adresse", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name="Téléhone", blank=True, null=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        ordering = ['nom']
