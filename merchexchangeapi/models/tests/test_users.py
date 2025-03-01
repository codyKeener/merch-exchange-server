## This test was written by ChatGPT

from django.test import TestCase

from merchexchangeapi.models import User, Listing, Artist, Category, WishlistListing
from decimal import Decimal

class UserModelTest(TestCase):

    def setUp(self):
        # Create test Artist, Category, and Listings for wishlist functionality
        self.artist = Artist.objects.create(name="Test Artist", genre="Rock")
        self.category = Category.objects.create(label="Test Category")
        
        self.user_data = {
            "username": "testuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "bio": "This is a test user.",
            "uid": "12345",
            "is_admin": False,
            "is_artist": False
        }

        # Create a User
        self.user = User.objects.create(**self.user_data)

        # Create a Listing associated with the User
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
            "sold": False
        }
        

    def test_create_user(self):
        user = User.objects.create(**self.user_data)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.bio, "This is a test user.")
        self.assertEqual(user.uid, "12345")
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_artist, False)

    def test_user_str_method(self):
        user = User.objects.create(**self.user_data)
        self.assertEqual(str(user), "testuser")
