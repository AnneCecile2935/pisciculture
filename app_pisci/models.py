from django.db import models
from django.utils import timezone # gestion du temps, date et heure

class TimeStampedModel(models.Model):
    """
    Classe de base abstraite pour ajouter automatiquement :
    - date_creation : date/heure de création
    - date_modification : date/heure de dernière modification
    """
    date_creation = models.DateField(
        verbose_name="Date de création",
        auto_now_add=True # Rempli automatiquement à la création
    )

    date_modification = models.DateField(
        verbose_name="Date de modification",
        auto_now=True # Mis à jour automatiquement à chaque modification
    )

    class Meta:
        abstract = True # Indique que cette classe ne crée pas de table en base

class Site(TimeStampedModel):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Bassin(TimeStampedModel):
    nom = models.CharField(max_length=100)
    site = models.ForeignKey('Site', on_delete=models.CASCADE) #si un site est supprimé, les bassins seront supprimés automatiquement

    def __str__(self):
        return self.nom

class ReleveTempOxy(TimeStampedModel):
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Température (°C)")
    oxygene = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Oxygène")

    def __str__(self):
        return f"Relevé du {self.date_creation} : {self.temperature}°C ({self.site.nom})"
