from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "booking", "amount", "payment_method", "payment_date"]
        read_only_fields = ["id", "payment_date"]
