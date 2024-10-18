from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    accessToken = models.CharField(blank=True, null=True)
    refreshToken = models.CharField(blank=True, null=True)
    tokenExpiry = models.DateTimeField(blank=True, null=True)
    creationDate = models.DateTimeField(auto_now=True)
