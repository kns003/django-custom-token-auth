'''
Generate token
'''
import time
from datetime import date, datetime

from django.utils import six
from django.utils.crypto import salted_hmac
from django.utils.http import base36_to_int, int_to_base36

from users.models import UserToken

class GenerateToken(object):
    """
    Strategy object used to generate and check tokens for the password
    reset mechanism.
    """
    key_salt = "django.contrib.auth.tokens.PasswordResetTokenGenerator"

    def make_token(self, user):
        """
        Returns a token that can be used once to do a password reset
        for the given user.
        """

        return self._make_token_with_timestamp(user, self._num_days(self._today()))

    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        # Parse the token
        try:
            ts_b36, hash = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError as e:
            return False

        # Check that the timestamp/uid has not been tampered with. ENABLE if Required
        # try:
        #     if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
        #         return False
        # except Exception as e:
        #     print ("exception", e)

        # Check the timestamp is within limit
        try:
            token_obj = UserToken.objects.get(access_token=token)
            if token_obj.expiry_date < datetime.now():
                return False
        except Exception as e:
            return False

        return True

    def _make_token_with_timestamp(self, user, timestamp):
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)

        # By hashing on the internal state of the user and using state
        # that is sure to change (the password salt will change as soon as
        # the password is set, at least for current Django auth, and
        # last_login will also change), we produce a hash that will be
        # invalid as soon as it is used.
        # We limit the hash to 20 chars to keep URL short
        try:
            hash = salted_hmac(
                self.key_salt,
                self._make_hash_value(user, timestamp),
            ).hexdigest()[::2]
        except Exception as e:
            raise ValueError(e)

        return "%s-%s" % (ts_b36, hash)

    def _make_hash_value(self, user, timestamp):
        # Ensure results are consistent across DB backends
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return (
            six.text_type(user.pk) + user.password +
            six.text_type(login_timestamp) + six.text_type(timestamp)
        )

    def _num_days(self, dt):
        return int(str(time.time()).split('.')[0])

    def _today(self):
        # Used for mocking in tests
        return date.today()
