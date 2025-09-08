from django.urls import path
from .views import ReviewListCreateView, ReviewDetailView

urlpatterns = [
    path(
        "<int:property_id>/", ReviewListCreateView.as_view(), name="review-list-create"
    ),
    path("detail/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
]
