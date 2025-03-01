## This test was written by ChatGPT

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from merchexchangeapi.models import User, Listing, Artist, Category, WishlistListing
from rest_framework.reverse import reverse
from decimal import Decimal

class UserViewSetTest(APITestCase):

    def setUp(self):
        # Create test Artist, Category, and Listing for the user's wishlist functionality
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

        # Create a User and Listing
        self.user = User.objects.create(**self.user_data)
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
        self.listing = Listing.objects.create(**self.listing_data)
        # Create WishlistListing to link User with Listing
        WishlistListing.objects.create(user=self.user, listing=self.listing)

        self.client = APIClient()

    def test_create_user(self):
        url = reverse('user-list')  # Assuming the URL name is 'user-list'
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], "testuser")

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return the created user

    def test_list_users_with_uid_filter(self):
        url = reverse('user-list') + "?uid=12345"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["uid"], "12345")

    def test_retrieve_user(self):
        url = reverse('user-detail', args=[self.user.id])  # Assuming URL name is 'user-detail'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testuser")
        
        # Since depth=1 is used in the UserSerializer, we expect the related 'wishlist_listings' to be serialized
        self.assertEqual(len(response.data['wishlist_listings']), 1)
        self.assertEqual(response.data['wishlist_listings'][0]['id'], self.listing.id)
        
        # Check the nested data for the listing (artist, category, etc.)
        listing_data = response.data['wishlist_listings'][0]
        self.assertEqual(listing_data['artist'], self.artist.id)
        self.assertEqual(listing_data['category'], self.category.id)
        self.assertEqual(listing_data['created_by'], self.user.id)

    def test_update_user(self):
        url = reverse('user-detail', args=[self.user.id])
        updated_data = {
            "username": "updateduser",
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated.user@example.com",
            "bio": "This is an updated test user.",
            "uid": "54321",
            "is_admin": True,
            "is_artist": False
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()  # Refresh the user instance
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.email, "updated.user@example.com")

    def test_delete_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

    def test_user_retrieve_with_wishlist(self):
        # Send a GET request to retrieve user data
        response = self.client.get(f'/users/{self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure wishlist listings are included in the response
        self.assertIn('wishlist_listings', response.data)
        self.assertEqual(len(response.data['wishlist_listings']), 1)
        
        # Check if the listing has nested fields as expected
        listing_data = response.data['wishlist_listings'][0]
        self.assertEqual(listing_data['artist'], self.artist.id)
        self.assertEqual(listing_data['category'], self.category.id)

    def test_user_list_with_wishlist(self):
        # Send a GET request to list users
        response = self.client.get('/users')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure wishlist listings are included in the response
        for user_data in response.data:
            self.assertIn('wishlist_listings', user_data)
            self.assertEqual(len(user_data['wishlist_listings']), 1)
            
            # Check if the listings contain nested fields (artist, category, etc.)
            for listing_data in user_data['wishlist_listings']:
                self.assertIn('artist', listing_data)
                self.assertIn('category', listing_data)
