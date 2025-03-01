## This test was written by ChatGPT

from rest_framework import status
from rest_framework.test import APITestCase
from merchexchangeapi.models import User, Listing, Artist, Category
from rest_framework.reverse import reverse

class UserIntegrationTests(APITestCase):
    
    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist", genre="Rock")
        self.category = Category.objects.create(label="Test Category")
        
        # Create test users
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "bio": "This is a test bio.",
            "uid": "123456",
            "is_admin": False,
            "is_artist": False,
        }
        
        self.user = User.objects.create(**self.user_data)
        
        # Create a test listing to associate with the user later
        self.listing = Listing.objects.create(
            title="Test Listing",
            artist=self.artist,
            category=self.category,
            description="A test description",
            price=100,
            size="Medium",
            condition="New",
            created_by=self.user,
            published=True,
            sold=False,
        )

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "bio": "This is a new user bio.",
            "uid": "654321",
            "is_admin": False,
            "is_artist": True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], "newuser")
        self.assertEqual(response.data['first_name'], "New")

    def test_retrieve_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['first_name'], self.user.first_name)

    def test_list_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one user created in setUp

    def test_update_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        updated_data = {
            "username": "updateduser",
            "first_name": "Updated",
            "last_name": "User",
            "email": "updateduser@example.com",
            "bio": "Updated bio.",
            "uid": "987654",
            "is_admin": True,
            "is_artist": False,
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "updateduser")
        self.assertEqual(response.data['first_name'], "Updated")

    def test_delete_user(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Confirm the user has been deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

    def test_user_wishlist_listings(self):
        # Create wishlist association with the user
        self.listing.wishlistlisting_set.create(user=self.user)
        
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure that the user's wishlist listings are included
        self.assertEqual(len(response.data['wishlist_listings']), 1)
        self.assertEqual(response.data['wishlist_listings'][0]['title'], self.listing.title)
