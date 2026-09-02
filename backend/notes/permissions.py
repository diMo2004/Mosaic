from rest_framework.permissions import BasePermission

class CanViewOwnNotes(BasePermission):
    """
    Custom permission to allow users to view their own notes.
    """
    message = "Viewing uploaded notes is available only for eligible contributor or premium account holders."
    def has_permission(self, request, view):
        # Check if the user is the owner of the note
        profile = getattr(request.user, 'profile', None)

        return bool(
            request.user
            and request.user.is_authenticated
            and profile
            and profile.can_view_own_notes
        )