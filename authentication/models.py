from django.contrib.auth.models import User
from django.db import models
from django_otp.plugins.otp_totp.models import TOTPDevice

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    totp_device = models.ForeignKey(TOTPDevice, null=True, blank=True, on_delete=models.CASCADE)
