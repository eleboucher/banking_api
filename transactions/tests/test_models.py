import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_create_transaction_success(transaction_factory):
    transaction = transaction_factory()
    assert transaction.transaction_id is not None
    assert transaction.amount is not None
    assert transaction.status in ["PENDING", "COMPLETED", "FAILED"]
    assert transaction.type in ["DEPOSIT", "WITHDRAWAL", "TRANSFER"]


@pytest.mark.django_db
def test_transaction_with_custom_data(transaction_factory, account_factory):
    from_acc = account_factory()
    to_acc = account_factory()
    transaction = transaction_factory(
        from_account=from_acc,
        to_account=to_acc,
        amount=1000.00,
        type="TRANSFER",
        status="COMPLETED",
        ref="Test transfer",
    )
    assert transaction.from_account == from_acc
    assert transaction.to_account == to_acc
    assert transaction.amount == 1000.00
    assert transaction.type == "TRANSFER"
    assert transaction.status == "COMPLETED"
    assert transaction.ref == "Test transfer"


@pytest.mark.django_db
def test_transaction_str_method(transaction_factory):
    transaction = transaction_factory()
    assert str(transaction) == str(transaction.transaction_id)


@pytest.mark.django_db
def test_transaction_without_accounts(transaction_factory):
    transaction = transaction_factory(
        from_account=None, to_account=None, type="DEPOSIT", status="PENDING"
    )
    assert transaction.from_account is None
    assert transaction.to_account is None


@pytest.mark.django_db
def test_transaction_amount_decimal_places(transaction_factory):
    transaction = transaction_factory(amount=100.55)
    assert float(transaction.amount) == 100.55


@pytest.mark.django_db
def test_transaction_invalid_type(transaction_factory):
    with pytest.raises(ValidationError):
        transaction = transaction_factory(type="INVALID")
        transaction.full_clean()


@pytest.mark.django_db
def test_transaction_invalid_status(transaction_factory):
    with pytest.raises(ValidationError):
        transaction = transaction_factory(status="INVALID")
        transaction.full_clean()


@pytest.mark.django_db
def test_transaction_negative_amount(transaction_factory):
    transaction = transaction_factory(amount=-100.00)
    assert float(transaction.amount) == -100.00


@pytest.mark.django_db
def test_transaction_created_at_auto_now(transaction_factory):
    transaction = transaction_factory()
    assert transaction.created_at is not None


@pytest.mark.django_db
def test_transaction_ref_optional(transaction_factory):
    transaction = transaction_factory(ref="")
    assert transaction.ref == ""
