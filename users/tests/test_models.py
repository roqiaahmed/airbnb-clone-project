import pytest
from users.models import User, UserRole


# def test_user_creation(django_user_model):
#     user = django_user_model.objects.create_user(
#         email="check@example.com",
#         password="StrongPass123!",
#         first_name="Check",
#         last_name="User",
#     )
#     assert user.id is not None
#     assert user.email == "check@example.com"


@pytest.mark.django_db
def test_user_str_returns_full_name_and_role(create_user):
    user = create_user(first_name="Ro", last_name="Ahmed", user_role=UserRole.HOST)
    assert str(user) == "Ro Ahmed (host)"


@pytest.mark.django_db
def test_user_default_role_is_guest(create_user):
    user = create_user()  # our fixture allows overriding
    # If user_role isn’t provided, it should default
    u = User.objects.get(id=user.id)
    assert u.user_role == UserRole.GUEST
