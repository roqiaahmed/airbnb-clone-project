from django.urls import path
from .views import BookingListCreateView, BookingRetrieveUpdateDeleteView

urlpatterns = [
    path("", BookingListCreateView.as_view(), name="booking-list-create"),
    path("<int:pk>/", BookingRetrieveUpdateDeleteView.as_view(), name="booking-detail"),
]
