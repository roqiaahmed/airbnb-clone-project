from django.urls import path, include
from .views import UserProfileView, RegisterView


urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("register/", RegisterView.as_view(), name="rest_register"),
]
