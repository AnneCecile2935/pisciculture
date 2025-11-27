from django.db import models
from apps.commun.models import TimeStampedModel

class Espece(TimeStampedModel):
    """
    Modèle représentant une espèce de poisson élevée dans les bassins de pisciculture.
    Chaque espèce est identifiée par un nom commun et un nom scientifique.
    Le champ `est_actif` permet de filtrer les espèces actuellement élevées.
    """
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
        verbose_name_plural = "Espèces"
        ordering = ['nom_commun']
        """
        Meta:
        - verbose_name (str): Nom singulier pour l'interface admin.
        - verbose_name_plural (str): Nom pluriel pour l'interface admin.
        - ordering (list): Trie les espèces par `nom_commun` dans les requêtes par défaut.
        """

    def __str__(self):
        """
        Retourne une représentation lisible de l'espèce, combinant son nom commun et son nom scientifique.

        Returns:
            str: Chaîne formatée "Nom commun (Nom scientifique)".
            Exemple : "Truite Arc en ciel (Oncorhynchus mykiss)".
        """
        return f"{self.nom_commun} ({self.nom_scientifique})"
