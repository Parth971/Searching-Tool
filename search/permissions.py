from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsSurveyFilled(BasePermission):
    """
    Permission class to check if the user has completed the survey.

    Attributes:
        message (str): The error message to be displayed when permission is denied.
    """

    message = "Permission denied. Please complete the survey"

    def has_permission(self, request, view):
        if not request.user.is_staff and not request.user.is_survey_completed:
            raise PermissionDenied(self.message)
        return True


class IsPreferenceOwner(BasePermission):
    """
        Permission class to check if the user is the owner of the preference.

        Attributes:
            message (str): The error message to be displayed when permission is denied.
        """

    message = "User does not have permission for this preference"

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.

        Args:
            request (HttpRequest): The request object.
            view (APIView): The view object.
            obj: The object being accessed.

        Returns:
            bool: True if the user is the owner of the preference, False otherwise.

        Raises:
            PermissionDenied: If the user is not the owner of the preference.
        """
        if request.user != obj.user:
            raise PermissionDenied(self.message)
        return True
