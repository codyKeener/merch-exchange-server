from django.db import models
from .user import User
from djmoney.models.fields import MoneyField
from .artist import Artist
from .category import Category

class Listing(models.Model):
  
  title = models.CharField(max_length=50)
  artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='listings')
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  description = models.CharField(max_length=280)
  price = MoneyField(max_digits=4, decimal_places=2, default_currency='USD')
  size = models.CharField(max_length=50)
  condition = models.CharField(max_length=50)
  image = models.URLField()
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
  created_at = models.DateTimeField(auto_now_add=True)
  published = models.BooleanField(default=False)
  sold = models.BooleanField(default=False)
  
  class Meta:
    ordering = ("-created_at", "artist", "title")
