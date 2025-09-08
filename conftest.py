import pytest
from rest_framework.test import APIClient
from django.conf import settings
from datetime import date, timedelta
from bookings.models import Booking
from listings.models import Listing
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def host_user(create_user):
    return create_user(
        email="host@test.com",
        password2="HostPass123!",
        password1="HostPass123!",
        user_role="host",
    )


@pytest.fixture
def guest_user(create_user):
    return create_user(
        email="guest@test.com",
        password2="GuestPass123!",
        password1="GuestPass123!",
        user_role="guest",
    )


@pytest.fixture
def user_payload():
    return {
        "email": "check@example.com",
        "password1": "StrongPass123!",
        "password2": "StrongPass123!",
        "first_name": "Ro",
        "last_name": "Ahmed",
        "phone_number": "+201234567890",
        "user_role": "guest",
    }


@pytest.fixture
def listing_payload():
    return {
        "title": "title for listing",
        "description": "description for listing",
        "price_per_night": 0,
        "location": "Egypt",
    }


@pytest.fixture
def booking_payload(listing_payload, guest_user):
    """Return a default payload for creating a booking."""
    return {
        "listing": None,
        # "user": None,  # To be set in tests
        "start_date": date.today(),
        "end_date": date.today() + timedelta(days=2),
    }


@pytest.fixture
def create_user(django_user_model):
    def _make_user(**kwargs):
        defaults = {
            "email": "user@example.com",
            "password": "StrongPass123!",
            "first_name": "Ro",
            "last_name": "Ahmed",
            "user_role": "guest",
            "phone_number": "+201234567890",
        }
        defaults.update(kwargs)
        # use create_user to ensure password is hashed
        user = django_user_model.objects.create_user(
            email=defaults["email"],
            password=defaults["password"],
            first_name=defaults["first_name"],
            last_name=defaults["last_name"],
            user_role=defaults["user_role"],
            phone_number=defaults["phone_number"],
        )
        return user

    return _make_user


@pytest.fixture
def booking(db):
    user = User.objects.create_user(
        email="guest@test.com", password="StrongPass123!", user_role="guest"
    )
    host = User.objects.create_user(
        email="host@test.com", password="HostPass123!", user_role="host"
    )
    listing = Listing.objects.create(
        host=host,
        title="Test Listing",
        description="Nice place",
        price_per_night=100,
        location="Cairo",
    )
    return Booking.objects.create(
        user=user,
        listing=listing,
        start_date="2025-09-10",
        end_date="2025-09-12",
        total_price=200,
    )
