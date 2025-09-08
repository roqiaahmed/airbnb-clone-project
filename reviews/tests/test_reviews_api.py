import pytest
from django.urls import reverse
from listings.models import Listing
from reviews.models import Review
from bookings.models import Booking, BookingStatus


@pytest.mark.django_db
def test_guest_without_booking_cannot_review(api_client, create_user, listing_payload):
    host = create_user(email="host@test.com", password="Host123!", role="host")
    guest = create_user(email="guest@test.com", password="Guest123!", role="guest")
    listing = Listing.objects.create(host=host, **listing_payload)

    api_client.force_authenticate(user=guest)
    url = reverse("review-list-create", args=[listing.id])
    payload = {"rating": 4, "comment": "Trying to cheat!"}
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "book this property" in str(response.data)


@pytest.mark.django_db
def test_guest_with_confirmed_booking_can_review(
    api_client, create_user, listing_payload
):
    host = create_user(email="host@test.com", password="Host123!", role="host")
    guest = create_user(email="guest@test.com", password="Guest123!", role="guest")
    listing = Listing.objects.create(host=host, **listing_payload)

    # confirmed booking
    Booking.objects.create(
        user=guest,
        listing=listing,
        start_date="2025-09-10",
        end_date="2025-09-12",
        total_price=200,
        status=BookingStatus.CONFIRMED,
    )

    api_client.force_authenticate(user=guest)
    url = reverse("review-list-create", args=[listing.id])
    payload = {"rating": 5, "comment": "Amazing place!"}
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Review.objects.count() == 1


@pytest.mark.django_db
def test_list_reviews(api_client, create_user, listing_payload):
    host = create_user(email="host@test.com", password="Host123!", role="host")
    guest = create_user(email="guest@test.com", password="Guest123!", role="guest")
    listing = Listing.objects.create(host=host, **listing_payload)

    Review.objects.create(property=listing, user=guest, rating=4, comment="Nice place!")

    url = reverse("review-list-create", args=[listing.id])
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["rating"] == 4


@pytest.mark.django_db
def test_update_review(api_client, create_user, listing_payload):
    host = create_user(email="host@test.com", password="Host123!", role="host")
    guest = create_user(email="guest@test.com", password="Guest123!", role="guest")
    listing = Listing.objects.create(host=host, **listing_payload)
    review = Review.objects.create(property=listing, user=guest, rating=3)

    api_client.force_authenticate(user=guest)
    url = reverse("review-detail", args=[review.id])
    response = api_client.patch(url, {"rating": 5}, format="json")

    assert response.status_code == 200
    review.refresh_from_db()
    assert review.rating == 5


@pytest.mark.django_db
def test_delete_review(api_client, create_user, listing_payload):
    host = create_user(email="host@test.com", password="Host123!", role="host")
    guest = create_user(email="guest@test.com", password="Guest123!", role="guest")
    listing = Listing.objects.create(host=host, **listing_payload)
    review = Review.objects.create(property=listing, user=guest, rating=3)

    api_client.force_authenticate(user=guest)
    url = reverse("review-detail", args=[review.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Review.objects.count() == 0
