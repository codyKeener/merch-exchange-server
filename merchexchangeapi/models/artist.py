from django.db import models

class Artist(models.Model):

    name = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
