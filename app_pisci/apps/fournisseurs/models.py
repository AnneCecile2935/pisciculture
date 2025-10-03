from django.db import models
from apps.commun.models import TimeStampedModel

class Fournisseurs(TimeStampedModel):
    TYPE_FOURNISSEUR_CHOICES= [
        ('ALIMENT', 'Aliment'),
        ('OEUFS', 'Oeufs'),
        ('MATERIEL', 'Matériel'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom du fournisseur")
    adresse = models.TextField(verbose_name="Adresse complète")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    code_postal = models.CharField(max_length=6, verbose_name="Code Postal")
    contact = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom de contact")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Adresse email")
    est_actif = models.BooleanField(default=True)
    type_fournisseur = models.CharField(
        max_length=20, choices=TYPE_FOURNISSEUR_CHOICES,
        verbose_name= "Type de fournisseur",
        help_text="Catégorie principale du fournisseur"
        )

    def __str__(self):
        return f"{self.nom} ({self.get_type_fournisseur_display()})"

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        permissions = [
            ("view_fournisseur", "Can view fournisseur"),
            ("add_fournisseur", "Can add fournisseur"),
            ("change_fournisseur", "Can change fournisseur"),
            ("delete_fournisseur", "Can delete fournisseur"),
        ]
        ordering = ['nom']
