import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.tests.factories import UserFactory
from accounts.tests.factories import AccountFactory
from transactions.tests.factories import TransactionFactory


@pytest.mark.django_db
class TestAccountTransactionViewSet:
    def setup_method(self):
        """
        This runs before each test, like setting up a fresh banking environment
        for each test scenario
        """
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create two accounts for this user
        self.account1 = AccountFactory(user=self.user, balance=1000)
        self.account2 = AccountFactory(user=self.user, balance=500)

        # Create some transactions
        self.transaction = TransactionFactory(
            from_account=self.account1, to_account=self.account2, amount=100
        )

    def test_user_can_view_own_account_transactions(self):
        """
        This test verifies that a user can see transactions for their account,
        like checking your bank statement
        """
        url = reverse(
            "account-transactions", kwargs={"account_id": self.account1.account_id}
        )
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["transaction_id"] == str(
            self.transaction.transaction_id
        )

    def test_user_cannot_view_other_user_transactions(self):
        """
        This test ensures users can't see transactions from accounts they don't own,
        like trying to look at someone else's bank statement
        """
        other_user = UserFactory()
        other_account = AccountFactory(user=other_user)

        url = reverse(
            "account-transactions", kwargs={"account_id": other_account.account_id}
        )
        response = self.client.get(url)

        assert response.status_code == 403

    def test_unauthenticated_user_cannot_view_transactions(self):
        """
        This test verifies that logged-out users can't view any transactions,
        like ensuring you need to show ID at the bank
        """
        self.client.force_authenticate(user=None)
        url = reverse(
            "account-transactions", kwargs={"account_id": self.account1.account_id}
        )
        response = self.client.get(url)

        assert response.status_code == 401
