import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError


@pytest.mark.django_db
def test_create_user_success(user_factory):
    user = user_factory()
    assert user.id is not None
    assert user.phone_number is not None
    assert user.date_of_birth is not None
    assert user.address is not None


@pytest.mark.django_db
def test_create_user_with_custom_data(user_factory):
    user = user_factory(
        phone_number="+1234567890",
        date_of_birth="1990-01-01",
        address="123 Test St",
    )
    assert user.phone_number == "+1234567890"


@pytest.mark.django_db
def test_user_str_method(user_factory):
    # Test the __str__ method returns email
    user = user_factory(email="test@example.com")
    assert str(user) == "test@example.com"


@pytest.mark.django_db
def test_phone_number_cannot_be_blank(user_factory):
    with pytest.raises(ValidationError):
        user = user_factory(phone_number="")
        user.full_clean()


@pytest.mark.django_db
def test_phone_number_unique(user_factory):
    # Create first user with phone number
    phone = "+1234567890"
    user_factory(phone_number=phone)

    # Try to create another user with same phone
    with pytest.raises(IntegrityError):
        user_factory(phone_number=phone)


@pytest.mark.django_db
def test_phone_number_cannot_be_null(user_factory):
    with pytest.raises(IntegrityError):
        user = user_factory(phone_number=None)
        user.full_clean()


@pytest.mark.django_db
def test_email_unique(user_factory):
    # Create first user
    email = "test@test.com"
    user_factory(email=email)

    # Try to create another user with same email
    with pytest.raises(IntegrityError):
        user = user_factory(email=email)
        user.full_clean()


@pytest.mark.django_db
def test_invalid_email_format(user_factory):
    with pytest.raises(ValidationError):
        user = user_factory(email="invalid-email", phone_number="+1234567890")
        user.full_clean()
