import factory
import uuid
from apps.aliments.models import Aliment
from apps.fournisseurs.tests.factories import FournisseurFactory

class AlimentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Aliment

    id = factory.LazyFunction(lambda: uuid.uuid4())
    nom = factory.Sequence(lambda n: f"Aliment {n}")
    code_alim = factory.Sequence(lambda n: f"AL{n:04d}")
    description = "Aliment test"
    fournisseur = factory.SubFactory(FournisseurFactory)
