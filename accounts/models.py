from django.db import models
from users.models import User
import uuid


class Account(models.Model):
    ACCOUNT_TYPES = [
        ("SAVINGS", "Savings"),
        ("CHECKING", "Checking"),
    ]

    ACCOUNT_STATUS = [
        ("ACTIVE", "Active"),
        ("FROZEN", "Frozen"),
        ("CLOSED", "Closed"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    status = models.CharField(max_length=16, choices=ACCOUNT_STATUS)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_id
