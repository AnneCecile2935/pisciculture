import factory
from apps.aliments.models import Aliment
from apps.fournisseurs.tests.factories import FournisseurFactory

class AlimentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Aliment

    nom = factory.Sequence(lambda n: f"Aliment {n}")
    code_alim = factory.Sequence(lambda n: f"CODE{n:02d}")
    description = factory.Faker("sentence")
    fournisseur = factory.SubFactory(FournisseurFactory)
