import factory
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    is_admin = False
    is_superuser = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("securepassword123")
        if create:
            self.save()

    @factory.post_generation
    def is_staff(self, create, extracted, **kwargs):
        self.is_staff = self.is_admin or self.is_superuser

class AdminUserFactory(UserFactory):
    is_admin = True
    is_superuser = True
