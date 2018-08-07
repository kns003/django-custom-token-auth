=====
Django Custom Token Authentication Using Django Rest Framework
=====

Quick start
-----------
1. `pip install django_custom_token_auth`

2. Add `custom_token` to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'custom_token',
    ]

3. Set timeout for your access token in `settings.py`.
TOKEN_EXPIRY_TIME_MINUTES = 60.
The value is in minutes. This can be set to the customized value in minutes

4. Name of the token. Usually tokens which will be sent from the client side will have hyphens instead of underscores.
But from the django side, the letters will be converted to caps and the hyphens whill be converted to undescores.

Example : `access-token` ==> `HTTP_ACCESS_TOKEN`

The above value can be customised according to requirements.

5.For all the views instead of inheriting from `APIView` we need to inherit from `CustomTokenAPIView`

Example :

`class UserList(CustomTokenAPIView):`
    `def get(self, request)`
        `....`
