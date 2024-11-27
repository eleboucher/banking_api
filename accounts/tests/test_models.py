import pytest
from datetime import datetime
from django.core.exceptions import ValidationError
from accounts.models import Account


@pytest.mark.django_db
def test_create_account_success(user_factory):
    user = user_factory()
    account = Account.objects.create(
        user=user, type="SAVINGS", status="ACTIVE", balance=1000.00
    )
    assert account.account_id is not None
    assert account.type == "SAVINGS"
    assert account.status == "ACTIVE"
    assert account.balance == 1000.00
    assert account.created_at is not None


@pytest.mark.django_db
def test_account_str_method(user_factory):
    user = user_factory()
    account = Account.objects.create(user=user, type="CHECKING", status="ACTIVE")
    assert str(account) == str(account.account_id)


@pytest.mark.django_db
def test_invalid_account_type(user_factory):
    user = user_factory()
    with pytest.raises(ValidationError):
        account = Account.objects.create(user=user, type="INVALID", status="ACTIVE")
        account.full_clean()


@pytest.mark.django_db
def test_invalid_account_status(user_factory):
    user = user_factory()
    with pytest.raises(ValidationError):
        account = Account.objects.create(user=user, type="SAVINGS", status="INVALID")
        account.full_clean()


@pytest.mark.django_db
def test_negative_balance(user_factory):
    user = user_factory()
    account = Account.objects.create(
        user=user, type="SAVINGS", status="ACTIVE", balance=-100.00
    )
    assert account.balance == -100.00


@pytest.mark.django_db
def test_delete_user_cascades_to_account(user_factory):
    user = user_factory()
    account = Account.objects.create(user=user, type="SAVINGS", status="ACTIVE")
    user.delete()
    with pytest.raises(Account.DoesNotExist):
        Account.objects.get(account_id=account.account_id)


@pytest.mark.django_db
def test_max_balance_digits(user_factory):
    user = user_factory()
    max_balance = 9999999999.99
    account = Account.objects.create(
        user=user, type="SAVINGS", status="ACTIVE", balance=max_balance
    )
    assert account.balance == max_balance
