import factory
from django.utils import timezone
from apps.activite_quotidien.models import Nourrissage
from apps.sites.tests.factories import SiteFactory, BassinFactory
from apps.stocks.tests.factories import LotDePoissonFactory
from apps.aliments.tests.factories import AlimentFactory
from apps.users.tests.factories import UserFactory

class NourrissageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Nourrissage
        # Retire skip_postgeneration_save pour permettre les sauvegardes automatiques
        # skip_postgeneration_save = True  # ← Commenté ou supprimé

    site_prod = factory.SubFactory(SiteFactory)
    aliment = factory.SubFactory(AlimentFactory)
    qte = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, min_value=0.01)
    date_repas = factory.Faker('date_this_year')
    cree_par = factory.SubFactory(UserFactory)
    notes = factory.Faker('text', max_nb_chars=100)

    @factory.lazy_attribute
    def crea_lot(self):
        """Crée un LotDePoisson avec un bassin lié au même site_prod."""
        # Utilise la factory LotDePoissonFactory qui gère déjà bassins
        return LotDePoissonFactory(site_prod=self.site_prod)

    @factory.lazy_attribute
    def bassin(self):
        """Crée un bassin lié au même site_prod que le nourrissage."""
        return BassinFactory(site=self.site_prod)

    @factory.post_generation
    def post_create(self, create, extracted, **kwargs):
        """Assure que le crea_lot est lié au bassin (si nécessaire).
        Note: Dans ton modèle, vérifie si cette relation est requise.
        """
        if create:
            # Si ton modèle Nourrissage a une relation directe avec Bassin,
            # ajoute-la ici. Sinon, cette méthode peut être supprimée.
            pass
