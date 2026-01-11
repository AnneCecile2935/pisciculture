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
        skip_postgeneration_save = True

    site_prod = factory.SubFactory(SiteFactory)
    aliment = factory.SubFactory(AlimentFactory)
    qte = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, min_value=0.01)
    date_repas = factory.Faker('date_this_year')
    cree_par = factory.SubFactory(UserFactory)
    notes = factory.Faker('text', max_nb_chars=100)

    @factory.lazy_attribute
    def bassin(self):
        """Crée un bassin lié au site_prod."""
        return BassinFactory(site=self.site_prod)

    @factory.lazy_attribute
    def crea_lot(self):
        """Crée un lot lié au bassin créé ci-dessus."""
        lot = LotDePoissonFactory(site_prod=self.site_prod)
        lot.bassins.add(self.bassin)  # Associe le bassin au lot
        return lot

    @factory.post_generation
    def post_create(self, create, extracted, **kwargs):
        """Sauvegarde l'instance après création."""
        if create:
            self.save()

