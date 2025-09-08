import pytest
from django.urls import reverse
from bookings.models import Booking
from payments.models import Payment, PaymentMethod


@pytest.mark.django_db
def test_create_payment(api_client, create_user, booking):
    user = booking.user
    api_client.force_authenticate(user=user)

    url = reverse("payment-create")
    payload = {
        "booking_id": booking.id,
        "payment_method": PaymentMethod.CREDIT_CARD,
        "amount": booking.total_price,
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == f"{booking.total_price:.2f}"  # serialized as string
    assert data["payment_method"] == PaymentMethod.CREDIT_CARD
    assert Payment.objects.count() == 1


@pytest.mark.django_db
def test_user_can_list_own_payments(api_client, create_user, booking):
    # create payment for this booking
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.total_price,
        payment_method=PaymentMethod.PAYPAL,
    )

    user = booking.user
    api_client.force_authenticate(user=user)

    url = reverse("payment-list")
    response = api_client.get(url)

    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["id"] == payment.id


@pytest.mark.django_db
def test_user_cannot_create_payment_for_other_booking(api_client, create_user, booking):
    # another user tries to pay for a booking they don’t own
    other_user = create_user(email="other@test.com", password="Other123!")
    api_client.force_authenticate(user=other_user)

    url = reverse("payment-create")
    payload = {
        "booking_id": booking.id,
        "payment_method": PaymentMethod.STRIPE,
        "amount": booking.total_price,
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "Invalid booking" in str(response.data)
    assert Payment.objects.count() == 0
