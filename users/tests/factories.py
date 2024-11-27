import factory

from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    phone_number = factory.Sequence(lambda n: f"+1555000{n:04}")
    date_of_birth = factory.Faker("date_of_birth", minimum_age=18)
    address = factory.Faker("address")
