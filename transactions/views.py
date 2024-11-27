from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class AccountTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # Add this to ensure user is authenticated

    # Instead of overriding dispatch, we'll use get_object
    def get_object(self):
        """
        This method is called by DRF to get the object the view is operating on.
        It's like having the teller verify your account before showing any information.
        """
        account = Account.objects.filter(
            account_id=self.kwargs["account_id"], user=self.request.user
        ).first()

        if not account:
            # Let DRF handle the 404 response properly
            self.permission_denied(
                self.request, message="Account not found or access denied."
            )

        return account

    def get_queryset(self):
        """
        This method gets called after get_object, so we know the account exists
        and belongs to the user.
        """
        account = self.get_object()
        return (
            Transaction.objects.filter(Q(from_account=account) | Q(to_account=account))
            .select_related("from_account", "to_account")
            .order_by("-created_at")
        )
