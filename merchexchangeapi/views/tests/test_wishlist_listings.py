## This test was written by ChatGPT

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.reverse import reverse
from merchexchangeapi.models import User, Listing, Artist, Category, WishlistListing

class WishlistListingViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(username='testuser', uid='12345')
        self.artist = Artist.objects.create(name='Test Artist')
        self.category = Category.objects.create(label='Test Category')
        self.listing = Listing.objects.create(
            title='Test Listing',
            artist=self.artist,
            category=self.category,
            description='A test listing description.',
            price=100.00,
            size='Medium',
            condition='New',
            image='http://example.com/image.jpg',
            created_by=self.user,
            published=True
        )

        self.wishlist_listing = WishlistListing.objects.create(
            user=self.user,
            listing=self.listing
        )

    def test_list_wishlist_listings(self):
        url = ('/wishlistlistings')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['id'], self.user.id)
        self.assertEqual(response.data[0]['listing']['id'], self.listing.id)

    def test_retrieve_wishlist_listing(self):
        url = reverse('wishlistlisting-detail', args=[self.wishlist_listing.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['listing']['id'], self.listing.id)

    def test_create_wishlist_listing(self):
        url = ('/wishlistlistings')
        data = {
            'user': self.user.id,
            'listing': self.listing.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishlistListing.objects.count(), 2)

    def test_update_wishlist_listing(self):
        url = reverse('wishlistlisting-detail', args=[self.wishlist_listing.id])
        new_user = User.objects.create(username='newuser', uid='67890')
        data = {
            'user': new_user.id,
            'listing': self.listing.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wishlist_listing.refresh_from_db()
        self.assertEqual(self.wishlist_listing.user.id, new_user.id)

    def test_delete_wishlist_listing(self):
        url = reverse('wishlistlisting-detail', args=[self.wishlist_listing.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WishlistListing.objects.count(), 0)
