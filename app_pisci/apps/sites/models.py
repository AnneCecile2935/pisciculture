from django.db import models
from apps.commun.models import TimeStampedModel
from django.core.validators import MinValueValidator

class Site(TimeStampedModel):
    """
    Modèle représentant un site de production piscicole.
    Un site regroupe plusieurs bassins et est identifié par un nom unique.
    """
    nom = models.CharField(max_length=100, unique=True)
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        """
        Retourne le nom du site.

        Returns:
            str: Nom du site.
        """
        return self.nom

class Bassin(TimeStampedModel):
    """
    Modèle représentant un bassin dans un site de production piscicole.
    Chaque bassin est associé à un site et peut avoir un volume et un type spécifiques.
    """
    nom = models.CharField(max_length=100)
    site = models.ForeignKey('sites.Site', on_delete=models.SET_NULL,null=True, related_name='bassins')
    volume = models.FloatField(blank=True, null=True, help_text="Volume en m3", validators=[MinValueValidator(0)])
    type = models.CharField(max_length=100, blank=True, null=True, help_text="categorie ecloserie, grossissement")
    est_actif= models.BooleanField(default=True)

    class Meta: #type: ignore
        unique_together = ('nom', 'site')
        """
        Meta:
        - unique_together (tuple): Garantit qu'un nom de bassin est unique par site.
        """
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.site.nom})"
