from rest_framework import permissions
from accounts.models import Account


class IsAccountOwner(permissions.BasePermission):
    """
    Custom permission to ensure only account owners can access their accounts.
    Like a bank's ID check system.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # This runs first, like the front door security
        # If we're looking at a specific account (detail view)
        if view.action in ["retrieve", "update", "partial_update", "destroy"]:
            account_id = view.kwargs.get("pk")
            return Account.objects.filter(
                account_id=account_id, user=request.user
            ).exists()
        return True

    def has_object_permission(self, request, view, obj):
        # This is like the teller's final verification
        return obj.user == request.user
