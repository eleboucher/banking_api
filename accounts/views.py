from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.models import Account
from accounts.serializers import AccountSerializer
from accounts.permissions import IsAccountOwner


class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAccountOwner]
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # When creating a new account, automatically assign it to the current user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def freeze(self, request, pk=None):
        # Special action to freeze an account, similar to putting a hold on a bank account
        account = self.get_object()
        account.status = "FROZEN"
        account.save()
        return Response({"status": "Account frozen"})

    @action(detail=True, methods=["get"])
    def balance(self, request, pk=None):
        # Quick way to check account balance, like using an ATM for balance inquiry
        account = self.get_object()
        return Response({"balance": account.balance})
