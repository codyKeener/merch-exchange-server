## This test was written by ChatGPT

from django.test import TestCase
from merchexchangeapi.models import User, Listing, Artist, Category, WishlistListing

class WishlistListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(uid="12345", username="testuser")
        self.artist = Artist.objects.create(name="Test Artist")
        self.category = Category.objects.create(label="Paintings")
        self.listing = Listing.objects.create(
            title="Test Listing",
            artist=self.artist,
            category=self.category,
            description="A beautiful piece of art",
            price=100.00,
            size="24x36",
            condition="New",
            image="http://example.com/image.jpg",
            created_by=self.user,
            published=True,
            sold=False
        )

    def test_create_wishlist_listing(self):
        wishlist_listing = WishlistListing.objects.create(user=self.user, listing=self.listing)

        self.assertEqual(wishlist_listing.user, self.user)
        self.assertEqual(wishlist_listing.listing, self.listing)

    def test_wishlist_listing_str(self):
        wishlist_listing = WishlistListing.objects.create(user=self.user, listing=self.listing)

        expected_str = f"{self.user.username} - {self.listing.title}"
        self.assertEqual(str(wishlist_listing), expected_str)

    def test_wishlist_listing_deletion(self):
        wishlist_listing = WishlistListing.objects.create(user=self.user, listing=self.listing)
        self.listing.delete()

        with self.assertRaises(WishlistListing.DoesNotExist):
            WishlistListing.objects.get(id=wishlist_listing.id)

    def test_wishlist_listing_user_deletion(self):
        wishlist_listing = WishlistListing.objects.create(user=self.user, listing=self.listing)
        self.user.delete()

        with self.assertRaises(WishlistListing.DoesNotExist):
            WishlistListing.objects.get(id=wishlist_listing.id)
