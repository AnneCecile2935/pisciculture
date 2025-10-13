import factory
import random
from apps.fournisseurs.models import Fournisseur

def generate_phone_number():
    # Génère un numéro de téléphone de 10 chiffres
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])


class FournisseurFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Fournisseur

    nom = factory.Sequence(lambda n: f"Fournisseur {n}")
    adresse = factory.Faker("street_address")
    ville = factory.Faker("city")
    code_postal = factory.Faker("postcode")
    contact = factory.Faker("name")
    telephone = factory.LazyFunction(generate_phone_number)
    email = factory.Faker("email")
    est_actif = True
    type_fournisseur = factory.Iterator(Fournisseur.TYPE_FOURNISSEUR_CHOICES, getter=lambda c: c[0])
