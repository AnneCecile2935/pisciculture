from django.db import models
from apps.commun.models import TimeStampedModel
from apps.sites.models import Site

class ReleveTempOxy(TimeStampedModel):
    MOMENT_CHOICES = [
        ('matin', 'Matin'),
        ('soir', 'Soir'),
    ]
    site = models.ForeignKey('sites.Site', on_delete=models.CASCADE, related_name='releves_temp_oxy')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Température (°C)")
    oxygene = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Oxygène (mg/L)")
    moment_jour = models.CharField(max_length=5, choices=MOMENT_CHOICES, verbose_name="Moment de la journée")

    def __str__(self):
        return f"Relevé du {self.date_creation.strftime('%d/%m/%Y')} ({self.get_moment_jour_display()}) : {self.temperature}°C, {self.oxygene} mg/L ({self.site.nom})"
