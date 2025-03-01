## This test was written by ChatGPT

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from merchexchangeapi.models import Listing, User, Artist, Category, WishlistListing

class ListingIntegrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            bio="An art lover and collector",
            uid="user123",
            is_admin=False,
            is_artist=False
        )
        self.artist = Artist.objects.create(name="Test Artist", genre="Abstract")
        self.category = Category.objects.create(label="Painting")
        self.listing = Listing.objects.create(
            title="Test Listing",
            artist=self.artist,
            category=self.category,
            description="A beautiful test painting",
            price="100.00",
            size="24x36",
            condition="New",
            image="http://example.com/image.jpg",
            created_by=self.user,
            published=True
        )
        self.wishlist_listing = WishlistListing.objects.create(user=self.user, listing=self.listing)

    def test_get_listing_list(self):
        url = reverse('listing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.listing.title)

    def test_create_listing(self):
        url = reverse('listing-list')
        data = {
            "title": "New Listing",
            "artist": self.artist.id,
            "category": self.category.id,
            "description": "A fresh new listing",
            "price": "200.00",
            "size": "18x24",
            "condition": "Excellent",
            "image": "http://example.com/new-image.jpg",
            "created_by": self.user.uid,
            "published": True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Listing.objects.count(), 2)

    def test_update_listing(self):
        url = reverse('listing-detail', args=[self.listing.id])
        data = {
            "title": "Updated Listing",
            "artist": self.artist.id,
            "category": self.category.id,
            "description": "An updated description",
            "price": "150.00",
            "size": "30x40",
            "condition": "Like New",
            "image": "http://example.com/updated-image.jpg",
            "created_by": self.user.uid,
            "published": False,
            "sold": True
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.title, "Updated Listing")

    def test_delete_listing(self):
        url = reverse('listing-detail', args=[self.listing.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Listing.objects.count(), 0)

    def test_filter_listings_by_artist(self):
        url = reverse('listing-list') + f'?artist={self.artist.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_wishlist_listing(self):
        url = reverse('wishlistlisting-list')
        data = {"user": self.user.id, "listing": self.listing.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishlistListing.objects.count(), 2)

if __name__ == '__main__':
    import unittest
    unittest.main()
