import pytest

from transactions.tests.factories import TransactionFactory
from accounts.tests.factories import AccountFactory


@pytest.fixture
def transaction_factory():
    return TransactionFactory


@pytest.fixture
def account_factory():
    return AccountFactory
