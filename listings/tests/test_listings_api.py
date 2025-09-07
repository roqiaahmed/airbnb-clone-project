import pytest
from django.urls import reverse
from listings.models import Listing


@pytest.mark.django_db
def test_guest_cannot_create_listing(api_client, guest_user):
    api_client.force_authenticate(user=guest_user)
    url = reverse("listing-create")
    response = api_client.post(url, {"title": "Nice place", "price_per_night": 100})
    assert response.status_code == 403  # forbidden
    assert Listing.objects.count() == 0


@pytest.mark.django_db
def test_host_can_create_listing(api_client, host_user, listing_payload):
    api_client.force_authenticate(user=host_user)
    url = reverse("listing-create")
    new_listing = {**listing_payload, "title": "Cozy House", "price_per_night": 150}
    response = api_client.post(url, new_listing)
    assert response.status_code == 201
    assert Listing.objects.count() == 1
    listing = Listing.objects.first()
    assert listing.host == host_user


@pytest.mark.django_db
def test_host_can_update_own_listing(api_client, host_user, listing_payload):
    listingPayload = {
        **listing_payload,
        "title": "Old Title",
        "price_per_night": 50,
        "host": host_user,
    }
    listing = Listing.objects.create(**listingPayload)
    api_client.force_authenticate(user=host_user)
    url = reverse("listing-detail", args=[listing.id])
    response = api_client.patch(url, {"title": "New Title"})
    assert response.status_code == 200
    listing.refresh_from_db()
    assert listing.title == "New Title"


@pytest.mark.django_db
def test_other_host_cannot_update_listing(
    api_client, create_user, host_user, listing_payload
):
    other_host = create_user(
        email="other@test.com", password="OtherPass123!", role="host"
    )
    listingPayload = {
        **listing_payload,
        "title": "Host1 Listing",
        "price_per_night": 80,
        "host": host_user,
    }
    listing = Listing.objects.create(**listingPayload)
    api_client.force_authenticate(user=other_host)
    url = reverse("listing-detail", args=[listing.id])
    response = api_client.patch(url, {"title": "Hacked Title"})
    assert response.status_code == 403
    listing.refresh_from_db()
    assert listing.title == "Host1 Listing"


@pytest.mark.django_db
def test_host_can_delete_own_listing(api_client, host_user, listing_payload):
    # create a listing owned by the host
    listing_data = {**listing_payload, "host": host_user}
    listing = Listing.objects.create(**listing_data)

    api_client.force_authenticate(user=host_user)
    url = reverse("listing-detail", args=[listing.id])

    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Listing.objects.filter(id=listing.id).exists()


@pytest.mark.django_db
def test_non_owner_cannot_delete_listing(
    api_client, host_user, guest_user, listing_payload
):
    # create a listing for host_user
    listing_data = {**listing_payload, "host": host_user}
    listing = Listing.objects.create(**listing_data)

    # try to delete as another normal user
    api_client.force_authenticate(user=guest_user)
    url = reverse("listing-detail", args=[listing.id])

    response = api_client.delete(url)

    assert response.status_code == 403  # Forbidden
    assert Listing.objects.filter(id=listing.id).exists()
