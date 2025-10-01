import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email',)

    email = factory.Faker('email')
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_admin = False

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Set the password after generation."""
        instance.set_password('testpass123')
        if create:
            instance.save()
