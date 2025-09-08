import pytest
from bookings.models import Booking
from payments.models import Payment, PaymentMethod


@pytest.mark.django_db
def test_create_payment(booking):
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.total_price,
        payment_method=PaymentMethod.CREDIT_CARD,
    )

    assert payment.id is not None
    assert payment.booking == booking
    assert payment.amount == booking.total_price
    assert payment.payment_method == PaymentMethod.CREDIT_CARD


@pytest.mark.django_db
def test_payment_str(booking):
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.total_price,
        payment_method=PaymentMethod.PAYPAL,
    )
    assert "paypal" in str(payment)
    assert str(payment.amount) in str(payment)
