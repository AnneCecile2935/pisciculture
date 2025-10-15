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
    bassin = factory.SubFactory(BassinFactory)
    crea_lot = factory.SubFactory(LotDePoissonFactory)
    aliment = factory.SubFactory(AlimentFactory)
    qte = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, min_value=0.01)
    date_repas = factory.Faker('date_this_year')
    cree_par = factory.SubFactory(UserFactory)
    notes = factory.Faker('text', max_nb_chars=100)

    @factory.post_generation
    def set_site_bassin(self, create, extracted, **kwargs):
        """Assure que le bassin appartient au site_prod."""
        if create and not extracted:
            self.bassin.site = self.site_prod
            self.bassin.save()
            self.crea_lot.bassin = self.bassin
            self.crea_lot.save()
