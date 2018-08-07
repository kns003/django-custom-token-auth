'''
Token based authentication
'''
import logging
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django_custom_token_auth.tokens import GenerateToken
from users.models import UserToken
logger = logging.getLogger(__name__)


class TokenBackend(ModelBackend):
    def authenticate(self, token=None):

        try:
            token_object = UserToken.objects.get(access_token=token)
        except Exception as e:
            return None

        if GenerateToken().check_token(token_object.guest, token_object.access_token):
            return token_object.guest
        else:
            return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
