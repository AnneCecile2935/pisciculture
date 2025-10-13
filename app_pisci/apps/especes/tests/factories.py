import factory
from apps.especes.models import Espece

class EspeceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Espece

    nom_commun = factory.Sequence(lambda n: f"Espèce {n}")
    nom_scientifique = factory.Sequence(lambda n: f"Scientifique {n}")
    est_actif = True
