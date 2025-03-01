## This test was written by ChatGPT

from rest_framework.test import APITestCase
from rest_framework import status
from merchexchangeapi.models import Artist
from rest_framework.reverse import reverse

class ArtistViewSetTest(APITestCase):

    def setUp(self):
        self.artist_data = {
            "name": "Test Artist",
            "genre": "Pop"
        }
        self.artist = Artist.objects.create(**self.artist_data)

    def test_create_artist(self):
        url = reverse('artist-list')  # Assuming the URL name is 'artist-list'
        data = {
            "name": "New Artist",
            "genre": "Rock"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Artist")
        self.assertEqual(response.data["genre"], "Rock")

    def test_list_artists(self):
        url = reverse('artist-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should be 1 since we added one artist in setUp
        self.assertEqual(response.data[0]["name"], self.artist.name)

    def test_retrieve_artist(self):
        url = reverse('artist-detail', args=[self.artist.id])  # Assuming URL name is 'artist-detail'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.artist.name)
        self.assertEqual(response.data["genre"], self.artist.genre)

    def test_update_artist(self):
        url = reverse('artist-detail', args=[self.artist.id])
        data = {
            "name": "Updated Artist",
            "genre": "Jazz"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.artist.refresh_from_db()  # Refresh the instance from the database
        self.assertEqual(self.artist.name, "Updated Artist")
        self.assertEqual(self.artist.genre, "Jazz")

    def test_delete_artist(self):
        url = reverse('artist-detail', args=[self.artist.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure artist was deleted
        with self.assertRaises(Artist.DoesNotExist):
            Artist.objects.get(id=self.artist.id)
    
    def test_artist_not_found(self):
        url = reverse('artist-detail', args=[9999])  # Non-existing ID
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Artist matching query does not exist.')
