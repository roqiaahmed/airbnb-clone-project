from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "listing",
            "start_date",
            "end_date",
            "total_price",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "total_price", "created_at", "updated_at"]

    def validate(self, data):
        start_date = data["start_date"]
        end_date = data["end_date"]
        listing = data["listing"]

        """Ensure end_date is after start_date."""
        if end_date <= start_date:
            raise serializers.ValidationError("End date must be after start date.")

        overlapping_bookings = Booking.objects.filter(
            listing=listing,
            status__in=["pending", "confirmed"],
            start_date__lt=end_date,
            end_date__gt=start_date,
        )

        # Exclude self if updating an existing booking
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError(
                "This listing is already booked for the selected dates."
            )

        return data
