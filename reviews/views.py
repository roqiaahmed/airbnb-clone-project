from rest_framework import generics, permissions, serializers
from .models import Review
from .serializers import ReviewSerializer
from listings.models import Listing
from bookings.models import Booking, BookingStatus


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        property_id = self.kwargs["property_id"]
        return Review.objects.filter(property_id=property_id)

    def perform_create(self, serializer):
        property_id = self.kwargs["property_id"]
        listing = Listing.objects.get(id=property_id)

        # ✅ check if the user has a confirmed booking
        has_booking = Booking.objects.filter(
            user=self.request.user, listing=listing, status=BookingStatus.CONFIRMED
        ).exists()

        if not has_booking:
            raise serializers.ValidationError(
                "You must book this property before reviewing."
            )

        serializer.save(user=self.request.user, property=listing)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionError("You cannot edit someone else’s review.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionError("You cannot delete someone else’s review.")
        instance.delete()
