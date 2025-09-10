from django.db import models
from apps.commun.models import TimeStampedModel

class Site(TimeStampedModel):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Bassin(TimeStampedModel):
    nom = models.CharField(max_length=100)
    site = models.ForeignKey('sites.Site', on_delete=models.CASCADE, related_name='bassins')

    def __str__(self):
        return f"{self.nom} ({self.site.nom})"
