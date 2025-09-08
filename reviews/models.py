from django.db import models
from django.conf import settings
from listings.models import Listing


class Review(models.Model):
    property = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("property", "user")  # user can only review a property once

    def __str__(self):
        return f"Review {self.rating}/5 by {self.user.email} on {self.property.title}"
