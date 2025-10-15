import factory
from apps.sites.models import Site, Bassin

class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site
        skip_postgeneration_save = True

    nom = factory.Sequence(lambda n: f"Site {n}")
    est_actif = True

class BassinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bassin

    nom = factory.Sequence(lambda n: f"Bassin {n}")
    site = factory.SubFactory(SiteFactory)
    volume = factory.Faker('pyfloat', positive=True, max_value=1000)
    type = factory.Faker('word')
    est_actif = True
