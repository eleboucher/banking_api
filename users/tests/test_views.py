import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserViewSet:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

    def test_get_own_profile(self):
        url = reverse("user-me")
        response = self.client.get(url)

        assert response.status_code == 200
        assert response.data["email"] == self.user.email
        assert response.data["phone_number"] == self.user.phone_number

    def test_update_profile_success(self):
        url = reverse("user-update-profile")
        update_data = {"phone_number": "+1987654321", "address": "New Address"}

        response = self.client.patch(url, update_data)

        assert response.status_code == 200
        assert response.data["phone_number"] == update_data["phone_number"]
        assert response.data["address"] == update_data["address"]

    def test_cannot_view_other_profiles(self):
        other_user = UserFactory()
        url = reverse("user-detail", kwargs={"pk": other_user.id})
        response = self.client.get(url)

        assert response.status_code == 404

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        url = reverse("user-me")
        response = self.client.get(url)

        assert response.status_code == 401

    def test_registration_success(self):
        self.client.force_authenticate(user=None)  # Ensure no authentication
        url = reverse("user-list")
        registration_data = {
            "email": "newuser@example.com",
            "phone_number": "+1234567890",
            "date_of_birth": "1990-01-01",
            "address": "Test Address",
        }

        response = self.client.post(url, registration_data)

        assert response.status_code == 201
        assert response.data["email"] == registration_data["email"]

    def test_registration_validation(self):
        self.client.force_authenticate(user=None)
        url = reverse("user-list")
        invalid_data = {
            "email": "invalid-email",  # Invalid email format
            "phone_number": "",  # Missing required field
        }

        response = self.client.post(url, invalid_data)

        assert response.status_code == 400
        assert "email" in response.data  # Should contain validation error for email
        assert (
            "phone_number" in response.data
        )  # Should contain validation error for phone

    def test_unique_fields_validation(self):
        self.client.force_authenticate(user=None)
        url = reverse("user-list")
        existing_user = UserFactory()
        duplicate_data = {
            "email": existing_user.email,
            "phone_number": "+1234567890",
        }

        response = self.client.post(url, duplicate_data)

        assert response.status_code == 400
        assert "email" in response.data  # Should indicate email already exists
