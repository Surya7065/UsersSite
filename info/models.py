from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class VerificationToken(models.Model):
    token = models.CharField(max_length=500)
    is_token_valid = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
