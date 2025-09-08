from rest_framework import generics, permissions, serializers
from .models import Payment
from .serializers import PaymentSerializer
from bookings.models import Booking


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking_id = self.request.data.get("booking_id")
        try:
            booking = Booking.objects.get(id=booking_id, user=self.request.user)
        except Booking.DoesNotExist:
            raise serializers.ValidationError("Invalid booking or permission denied.")

        serializer.save(booking=booking, amount=booking.total_price)


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # show only the user’s payments
        return Payment.objects.filter(booking__user=self.request.user)
