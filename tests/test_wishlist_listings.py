from rest_framework import status
from rest_framework.test import APITestCase
from merchexchangeapi.models import WishlistListing, User, Listing, Artist, Category
from rest_framework.reverse import reverse

class WishlistListingIntegrationTests(APITestCase):

    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist", genre="Rock")
        self.category = Category.objects.create(label="Test Category")
      
        # Create test users and listings
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

        # Create a WishlistListing association between the user and the listing
        self.wishlist_listing = WishlistListing.objects.create(
            user=self.user,
            listing=self.listing
        )

    def test_create_wishlist_listing(self):
        url = reverse('wishlistlisting-list')
        data = {
            "user": self.user.id,
            "listing": self.listing.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['listing']['id'], self.listing.id)

    def test_retrieve_wishlist_listing(self):
        url = reverse('wishlistlisting-detail', kwargs={'pk': self.wishlist_listing.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['listing']['id'], self.listing.id)

    def test_list_wishlist_listings(self):
        url = reverse('wishlistlisting-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one wishlist listing created in setUp

    def test_update_wishlist_listing(self):
        url = reverse('wishlistlisting-detail', kwargs={'pk': self.wishlist_listing.id})
        # Create another user and listing to update the wishlist listing
        new_user = User.objects.create(username="newuser", email="newuser@example.com", uid="654321")
        new_listing = Listing.objects.create(title="New Test Listing", artist=self.artist, category=self.category, description="Another test description", price=150, size="Large", condition="Used", created_by=self.user, published=True, sold=False)

        updated_data = {
            "user": new_user.id,
            "listing": new_listing.id
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], new_user.id)
        self.assertEqual(response.data['listing']['id'], new_listing.id)

    def test_delete_wishlist_listing(self):
        url = reverse('wishlistlisting-detail', kwargs={'pk': self.wishlist_listing.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Confirm the wishlist listing has been deleted
        with self.assertRaises(WishlistListing.DoesNotExist):
            WishlistListing.objects.get(id=self.wishlist_listing.id)
