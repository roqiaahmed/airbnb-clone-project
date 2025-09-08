from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    property = serializers.ReadOnlyField(source="property.id")

    class Meta:
        model = Review
        fields = [
            "id",
            "property",
            "user",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
