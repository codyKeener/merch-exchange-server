from django.db import models

class User(models.Model):

    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    bio = models.CharField(max_length=400)
    uid = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
