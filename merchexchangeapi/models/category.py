from django.db import models

class Category(models.Model):

    label = models.CharField(max_length=50)
    image = models.URLField()

    def __str__(self):
        return self.label
