from django.db.models import Manager


class FrameworkModelManager(Manager):
    """
    Custom manager for the Framework model.

    Methods:
        get_user_preferences(user, preference_names=None): Retrieves the user preferences for frameworks.
    """

    def get_user_preferences(self, user, preference_names=None):
        """
        Retrieves the user preferences for frameworks.

        Args:
            user (User): The user object.
            preference_names (list, optional): List of preference names to filter. Defaults to None.

        Returns:
            QuerySet: The queryset of Framework objects matching the user preferences.
        """
        queryset = self.model.objects.filter(preferences__user=user)
        if preference_names is not None:
            queryset.filter(name__in=preference_names)
        return queryset
