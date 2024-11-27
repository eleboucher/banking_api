import factory


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "transactions.Transaction"

    from_account = factory.SubFactory("accounts.tests.factories.AccountFactory")
    to_account = factory.SubFactory("accounts.tests.factories.AccountFactory")
    type = "DEPOSIT"
    amount = 1000.00
    status = "PENDING"
    created_at = factory.Faker("date_time_this_year")
