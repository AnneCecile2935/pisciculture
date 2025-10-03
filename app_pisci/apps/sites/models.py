from django.db import models
from apps.commun.models import TimeStampedModel

class Site(TimeStampedModel):
    nom = models.CharField(max_length=100)
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

class Bassin(TimeStampedModel):
    nom = models.CharField(max_length=100)
    site = models.ForeignKey('sites.Site', on_delete=models.CASCADE, related_name='bassins')
    volume = models.FloatField(blank=True, null=True, help_text="Volume en m3")
    type = models.CharField(max_length=100, blank=True, null=True, help_text="categorie ecloserie, grossissement")
    est_actif= models.BooleanField(default=True)

    class Meta:
        unique_together = ('nom', 'site')
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.site.nom})"
