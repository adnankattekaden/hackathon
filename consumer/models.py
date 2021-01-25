from django.db import models
from django.contrib.auth.models import User,auth

# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.BigIntegerField(null=True,blank=True)
