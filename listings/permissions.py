from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsHostAndOwner(BasePermission):
    """
    Allow only hosts to create listings.
    Allow only the host who owns the listing to update/delete it.
    """

    def has_permission(self, request, view):
        # For create: must be authenticated and a host
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated and request.user.user_role == "host"
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For update/delete: must be the owner
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return obj.host == request.user
        return True
