from django.db import models
from bookings.models import Booking


class PaymentMethod(models.TextChoices):
    CREDIT_CARD = "credit_card", "Credit Card"
    PAYPAL = "paypal", "PayPal"
    STRIPE = "stripe", "Stripe"


class Payment(models.Model):
    booking = models.OneToOneField(  # each booking has exactly one payment
        Booking, on_delete=models.CASCADE, related_name="payment"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.amount} via {self.payment_method}"
