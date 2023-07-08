from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import ValidationError

from accounts.constants import INVALID_UID, INVALID_TOKEN
from accounts.models import User


class ValidateRestorePassword:
    token_generator = PasswordResetTokenGenerator()

    def __init__(self):
        self.kwargs = None
        self.user = None

    def is_token_valid(self, token):
        return self.token_generator.check_token(self.user, token)

    def is_uid_valid(self, uid):
        self.user = User.get_object(query={'id': uid})
        return self.user

    def validate(self, uid, token):
        if not self.is_uid_valid(uid):
            raise ValidationError({'message': INVALID_UID})

        if not self.is_token_valid(token):
            raise ValidationError({'message': INVALID_TOKEN})

    def get_object(self):
        token = self.kwargs.get('token')
        uid = self.kwargs.get('uid')
        self.validate(uid, token)
        return self.user
