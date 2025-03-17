from django.db import models

class Artist(models.Model):

    name = models.CharField(max_length=100, unique=True)
    genre = models.CharField(max_length=50)
    
    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name
    