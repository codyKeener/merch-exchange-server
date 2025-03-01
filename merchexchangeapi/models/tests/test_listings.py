## This test was written by ChatGPT

from django.test import TestCase
from merchexchangeapi.models import Listing, Artist, Category, User
from decimal import Decimal

class ListingModelTest(TestCase):

    def setUp(self):
        # Create test Artist, Category, and User
        self.artist = Artist.objects.create(name="Test Artist", genre="Rock")
        self.category = Category.objects.create(label="Test Category")
        self.user = User.objects.create(username="testuser", uid="12345")
        
        self.listing_data = {
            "title": "Test Listing",
            "artist": self.artist,
            "category": self.category,
            "description": "This is a test listing",
            "price": Decimal('10.00'),
            "size": "Medium",
            "condition": "New",
            "image": "http://example.com/image.jpg",
            "created_by": self.user,
            "published": False,
        }

    def test_create_listing(self):
        listing = Listing.objects.create(**self.listing_data)
        self.assertEqual(listing.title, "Test Listing")
        self.assertEqual(listing.artist.name, "Test Artist")
        self.assertEqual(listing.category.label, "Test Category")
        self.assertEqual(listing.price, Decimal('10.00'))
        self.assertEqual(listing.size, "Medium")
        self.assertEqual(listing.condition, "New")
        self.assertEqual(listing.created_by.username, "testuser")

    def test_listing_str_method(self):
        listing = Listing.objects.create(**self.listing_data)
        self.assertEqual(str(listing), "Test Listing")
