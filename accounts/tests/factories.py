from decimal import Decimal
import factory
from accounts.models import Account


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    user = factory.SubFactory("users.tests.factories.UserFactory")
    account_id = factory.Faker("uuid4")
    type = factory.Iterator(["SAVINGS", "CHECKING"])
    status = factory.Iterator(["ACTIVE", "FROZEN", "CLOSED"])
    balance = factory.LazyFunction(lambda: Decimal("0.00"))
    created_at = factory.Faker("date_time")
