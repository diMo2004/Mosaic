from rest_framework.permissions import BasePermission

class IsProfileComplete(BasePermission):
    """
    Allows access only to users with a complete profile.
    """
    message = "Profile completion is required to access this resource."

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        profile = getattr(user, 'profile', None)
        return bool(profile and profile.profile_completed)