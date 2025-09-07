import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_user(api_client, user_payload):
    url = reverse("rest_register")
    response = api_client.post(url, user_payload, format="json")
    data = response.json()
    assert response.status_code == 201

    assert data["email"] == user_payload["email"]
    assert data["first_name"] == user_payload["first_name"]
    assert data["phone_number"] == user_payload["phone_number"]
    assert data["user_role"] == user_payload["user_role"]


@pytest.mark.django_db
def test_login_user(api_client, create_user):
    user = create_user(email="login@test.com", password="StrongPass123!")
    url = reverse("jwt_create")
    response = api_client.post(
        url,
        {"email": user.email, "password": "StrongPass123!"},
        format="json",
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data or "access" in data


@pytest.mark.django_db
def test_refresh_token(api_client, create_user):
    # Arrange: create user and login to get tokens
    create_user(email="refresh@test.com", password="StrongPass123!")
    login_url = reverse("jwt_create")
    login_response = api_client.post(
        login_url,
        {"email": "refresh@test.com", "password": "StrongPass123!"},
        format="json",
    )
    refresh_token = login_response.data["refresh"]

    # Act: send refresh token to refresh endpoint
    refresh_url = reverse("jwt_refresh")
    response = api_client.post(refresh_url, {"refresh": refresh_token}, format="json")

    # Assert: new access token returned
    assert response.status_code == 200
    assert "access" in response.data
