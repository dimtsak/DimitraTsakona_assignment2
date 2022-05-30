from django.db import models
from django.contrib.auth.models import User

class Trainer(models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    subject = models.CharField(max_length=45)

class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_moderator = models.BooleanField(default=False)