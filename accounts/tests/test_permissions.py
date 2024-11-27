import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.tests.factories import UserFactory
from accounts.tests.factories import AccountFactory
from accounts.permissions import IsAccountOwner


@pytest.mark.django_db
class TestIsAccountOwnerPermission:
    def setup_method(self):
        self.permission = IsAccountOwner()
        self.client = APIClient()
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.account = AccountFactory(user=self.user)

    def test_owner_has_permission(self):
        request = type("Request", (), {"user": self.user})()
        obj = type("Object", (), {"user": self.user})()
        assert self.permission.has_object_permission(request, None, obj) is True

    def test_non_owner_has_no_permission(self):
        request = type("Request", (), {"user": self.other_user})()
        obj = type("Object", (), {"user": self.user})()
        assert self.permission.has_object_permission(request, None, obj) is False

    def test_unauthenticated_user_has_no_permission(self):
        request = type("Request", (), {"user": None})()
        obj = type("Object", (), {"user": self.user})()
        assert self.permission.has_object_permission(request, None, obj) is False

    def test_superuser_has_no_permission(self):
        self.other_user.is_superuser = True
        request = type("Request", (), {"user": self.other_user})()
        obj = type("Object", (), {"user": self.user})()
        assert self.permission.has_object_permission(request, None, obj) is False
