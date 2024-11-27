from django.db import models
import uuid

from accounts.models import Account


class Transaction(models.Model):
    TRANSACTION_STATUS = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]
    TRANSACTION_TYPES = [
        ("DEPOSIT", "Deposit"),
        ("WITHDRAWAL", "Withdrawal"),
        ("TRANSFER", "Transfer"),
    ]
    transaction_id = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4
    )
    from_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="debits", null=True
    )
    to_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="credits", null=True
    )
    type = models.CharField(max_length=12, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=12, choices=TRANSACTION_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    ref = models.TextField(blank=True)

    def __str__(self):
        return self.transaction_id
