import factory
from apps.stocks.models import LotDePoisson
from apps.especes.tests.factories import EspeceFactory
from apps.sites.tests.factories import SiteFactory, BassinFactory
from apps.fournisseurs.tests.factories import FournisseurFactory
from django.utils import timezone

class LotDePoissonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LotDePoisson

    espece = factory.SubFactory(EspeceFactory)
    site_prod = factory.SubFactory(SiteFactory)
    fournisseur = factory.SubFactory(FournisseurFactory)
    @factory.lazy_attribute
    def bassin(self):
        return BassinFactory(site=self.site_prod)

    date_arrivee = factory.LazyFunction(timezone.now)
    quantite = factory.Faker("random_int", min=100, max=10000)
    quantite_actuelle = factory.LazyAttribute(lambda o: o.quantite)
    statut = "OEUF"
    code_lot = factory.Sequence(lambda n: f"LOT{n:04d}")
    poids = factory.Faker("random_int", min=1, max=100)
    poids_moyen = None  # Calculé automatiquement dans save()
