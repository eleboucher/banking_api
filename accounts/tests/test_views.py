import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.tests.factories import AccountFactory
from decimal import Decimal

from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestAccountViewSet:
    def setup_method(self):
        # First, we set up our testing environment, just like preparing a test environment
        # at a bank where we can safely try different account operations
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        # Create a test account that we'll use in many of our tests
        self.account = AccountFactory(
            user=self.user, balance=Decimal("1000.00"), status="ACTIVE", type="SAVINGS"
        )

    def test_list_own_accounts(self):
        # This test verifies that users can see all their accounts,
        # similar to how you'd check if a bank's account listing feature works

        # Create an additional account for our user
        AccountFactory(user=self.user, type="CHECKING")
        # Create another user's account that shouldn't be visible
        AccountFactory(user=UserFactory())

        url = reverse("account-list")
        response = self.client.get(url)

        # Verify the response contains exactly our user's accounts
        assert response.status_code == 200
        assert len(response.data) == 2  # Should only see their own accounts

    def test_create_account(self):
        # Tests account creation, like opening a new bank account
        url = reverse("account-list")
        account_data = {"type": "CHECKING"}

        response = self.client.post(url, account_data)
        print(response.data)
        assert response.status_code == 201
        assert response.data["type"] == "CHECKING"
        assert response.data["status"] == "ACTIVE"  # Should start active
        assert response.data["balance"] == "0.00"  # Should start with zero balance

    def test_get_account_details(self):
        # Verifies that account detail retrieval works correctly
        url = reverse("account-detail", kwargs={"pk": self.account.account_id})
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.data["account_id"] == str(self.account.account_id)
        assert response.data["type"] == self.account.type
        assert response.data["balance"] == str(self.account.balance)

    def test_cannot_view_others_account(self):
        # Tests privacy - users shouldn't be able to see others' accounts,
        # just like how bank customers can't view each other's accounts
        other_account = AccountFactory(user=UserFactory())

        url = reverse("account-detail", kwargs={"pk": other_account.account_id})
        response = self.client.get(url)

        assert response.status_code == 403

    def test_freeze_account(self):
        # Tests the special action to freeze an account
        url = reverse("account-freeze", kwargs={"pk": self.account.account_id})
        response = self.client.post(url)

        assert response.status_code == 200

        # Verify the account is actually frozen in the database
        self.account.refresh_from_db()
        assert self.account.status == "FROZEN"

    def test_check_balance(self):
        # Tests the balance checking endpoint
        url = reverse("account-balance", kwargs={"pk": self.account.account_id})
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.data["balance"] == self.account.balance

    def test_cannot_modify_balance_directly(self):
        # Verifies that balance can't be changed through regular updates,
        # similar to how customers can't just "edit" their balance at a bank
        url = reverse("account-detail", kwargs={"pk": self.account.account_id})
        update_data = {"balance": "9999999.99"}  # Attempting to change balance

        response = self.client.patch(url, update_data)

        # Verify the balance hasn't changed
        self.account.refresh_from_db()
        assert self.account.balance == Decimal("1000.00")

    def test_unauthenticated_access(self):
        # Verifies that unauthenticated users can't access accounts
        self.client.force_authenticate(user=None)
        url = reverse("account-list")
        response = self.client.get(url)

        assert response.status_code == 401
