from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Listing
        fields = [
            "id",
            "host",
            "title",
            "description",
            "price_per_night",
            "location",
            "created_at",
        ]
        read_only_fields = ["id", "host", "created_at"]
