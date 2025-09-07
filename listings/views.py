from rest_framework import generics, permissions
from .models import Listing
from .serializers import ListingSerializer
from .permissions import IsHostAndOwner


class ListingListCreateView(generics.ListCreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsHostAndOwner]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsHostAndOwner]
