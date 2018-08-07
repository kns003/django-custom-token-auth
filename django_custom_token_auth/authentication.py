import logging
import requests

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from .backends import TokenBackend

auth_logger = logging.getLogger(__name__)


class VerifyApiAndUserAuthentication(TokenAuthentication):
    def __init__(self, *args, **kwargs):
        super(VerifyApiAndUserAuthentication, self).__init__(*args, **kwargs)
        self.backend = TokenBackend()

    def authenticate(self, request, **kwargs):

        if request.META[settings.HTTP_ACCESS_TOKEN]:
            user = self.backend.authenticate(
                token=request.META[settings.HTTP_ACCESS_TOKEN]
            )
            if user:
                return (user, request.META[settings.HTTP_ACCESS_TOKEN])
            else:
                raise exceptions.NotAuthenticated("Invalid token")
        else:
            raise exceptions.NotAcceptable(_('Access token not present'))
