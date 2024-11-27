from rest_framework import serializers
from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["account_id", "type", "balance", "status", "created_at"]
        read_only_fields = ["account_id", "balance", "created_at"]
