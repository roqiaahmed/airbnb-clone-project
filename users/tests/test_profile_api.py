import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_profile_requires_authentication(api_client):
    url = reverse("user-profile")
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_authenticated_user_can_get_profile(api_client, create_user):
    user = create_user(email="me@test.com", password="StrongPass123!")
    api_client.force_authenticate(user=user)  # shortcut to skip login
    url = reverse("user-profile")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()["email"] == "me@test.com"


@pytest.mark.django_db
def test_authenticated_user_can_update_profile(api_client, create_user):
    user = create_user(email="me2@test.com", password="StrongPass123!")
    api_client.force_authenticate(user=user)
    url = reverse("user-profile")
    response = api_client.patch(url, {"first_name": "Updated"}, format="json")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"
