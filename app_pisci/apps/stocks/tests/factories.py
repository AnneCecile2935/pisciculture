import factory
from apps.stocks.models import LotDePoisson
from apps.especes.tests.factories import EspeceFactory
from apps.sites.tests.factories import SiteFactory, BassinFactory
from apps.fournisseurs.tests.factories import FournisseurFactory
from django.utils import timezone

class LotDePoissonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LotDePoisson
        skip_postgeneration_save = True

    espece = factory.SubFactory(EspeceFactory)
    site_prod = factory.SubFactory(SiteFactory)
    fournisseur = factory.SubFactory(FournisseurFactory)
    date_arrivee = factory.LazyFunction(timezone.now)
    quantite = factory.Faker("random_int", min=100, max=10000)
    quantite_actuelle = factory.LazyAttribute(lambda o: o.quantite)  # Par défaut = quantite
    statut = "OEUF"
    code_lot = factory.Sequence(lambda n: f"LOT{n:04d}")  # Formatage plus propre (LOT0001)
    poids = factory.Faker("pyfloat", positive=True, max_value=100)  # Poids réaliste

    @factory.post_generation
    def bassins(self, create, extracted, **kwargs):
        """Gère la relation ManyToMany avec Bassin.
        Usage:
            - LotDePoissonFactory() → 1 bassin aléatoire
            - LotDePoissonFactory(bassins=[bassin1, bassin2]) → bassins spécifiques
        """
        if not create:
            return
        if extracted:  # Si des bassins sont passés explicitement
            for bassin in extracted:
                self.bassins.add(bassin)
        else:  # Sinon, ajoute un bassin par défaut
            self.bassins.add(BassinFactory(site=self.site_prod))  # Lie le bassin au même site
