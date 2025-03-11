from django.db import models

class User(models.Model):

    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    bio = models.CharField(max_length=400)
    profile_pic = models.URLField()
    uid = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
