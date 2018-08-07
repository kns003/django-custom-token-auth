from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.

def token_expiry_date():
    return datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRY_TIME_MINUTES)


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    access_token = models.CharField(max_length=200, null=True, blank=True)
    expiry_date = models.DateTimeField(default=token_expiry_date)