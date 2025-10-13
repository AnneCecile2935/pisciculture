from django.db import models
from apps.commun.models import TimeStampedModel
from apps.fournisseurs.models import Fournisseur

class Aliment(TimeStampedModel):
    nom = models.CharField(max_length=50, unique=True, verbose_name="Nom de l'aliment")
    code_alim = models.CharField(max_length=6, unique=True, verbose_name="Code nom de l'aliment")
    description = models.TextField(blank=True, verbose_name="Description", help_text="Description détaillée de l'aliment")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.RESTRICT, related_name="aliments", verbose_name="Fournisseur", help_text="Fournisseur de l'aliment")

    class Meta: 
        verbose_name = "Aliment"
        verbose_name_plural = "Aliments"
        ordering = ["code_alim"]

    def __str__(self):
        return f"{self.nom} (Fournisseur: {self.fournisseur.nom})"
