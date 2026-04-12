import factory
from django.contrib.auth import get_user_model

User = get_user_model()


import factory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")

    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "pass1234"
        self.set_password(password)
        if create:
            self.save()


class AdminUserFactory(UserFactory):
    is_staff = True
    is_superuser = True
