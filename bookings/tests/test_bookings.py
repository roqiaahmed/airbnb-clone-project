import pytest
from django.urls import reverse
from listings.models import Listing
from bookings.models import Booking
from datetime import date, timedelta


@pytest.mark.django_db
def test_create_booking(api_client, guest_user, host_user, booking_payload):
    # Create a listing
    listing = Listing.objects.create(
        host=host_user,
        title="Test Listing",
        description="Test description",
        price_per_night=100,
        location="Cairo",
    )

    api_client.force_authenticate(user=guest_user)

    payload = booking_payload.copy()
    payload["listing"] = listing.id

    url = reverse("booking-list-create")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    data = response.json()
    assert data["total_price"] == "200.00"
    assert data["status"] == "pending"


@pytest.mark.django_db
def test_prevent_overlapping_booking(
    api_client, guest_user, host_user, booking_payload
):
    listing = Listing.objects.create(
        host=host_user,
        title="Test Listing",
        description="Test description",
        price_per_night=100,
        location="Cairo",
    )

    # Existing booking
    Booking.objects.create(
        user=guest_user,
        listing=listing,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=3),
        total_price=300,
        status="confirmed",
    )

    api_client.force_authenticate(user=guest_user)

    payload = booking_payload.copy()
    payload["listing"] = listing.id
    payload["start_date"] = date.today() + timedelta(days=1)
    payload["end_date"] = date.today() + timedelta(days=4)

    url = reverse("booking-list-create")
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "already booked" in response.json()["non_field_errors"][0]


@pytest.mark.django_db
def test_user_can_only_update_own_booking(
    api_client, guest_user, host_user, create_user, booking_payload
):
    listing = Listing.objects.create(
        host=host_user,
        title="Test Listing",
        description="Test description",
        price_per_night=100,
        location="Cairo",
    )

    other_user = create_user(email="other@test.com")

    booking = Booking.objects.create(
        user=other_user,
        listing=listing,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1),
        total_price=100,
        status="pending",
    )

    api_client.force_authenticate(user=guest_user)

    url = reverse("booking-detail", args=[booking.id])
    response = api_client.patch(url, {"status": "confirmed"}, format="json")

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_can_delete_own_booking(
    api_client, guest_user, host_user, booking_payload
):
    listing = Listing.objects.create(
        host=host_user,
        title="Test Listing",
        description="Test description",
        price_per_night=100,
        location="Cairo",
    )

    booking = Booking.objects.create(
        user=guest_user,
        listing=listing,
        start_date=booking_payload["start_date"],
        end_date=booking_payload["end_date"],
        total_price=200,
        status="pending",
    )

    api_client.force_authenticate(user=guest_user)

    url = reverse("booking-detail", args=[booking.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Booking.objects.filter(id=booking.id).count() == 0
