## This test was written by ChatGPT
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from merchexchangeapi.models import Artist

class ArtistIntegrationTests(APITestCase):

    def setUp(self):
        self.artist = Artist.objects.create(name='Test Artist', genre='Rock')

    def test_get_artist_list(self):
        url = reverse('artist-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Artist')

    def test_get_single_artist(self):
        url = reverse('artist-detail', args=[self.artist.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Artist')
        self.assertEqual(response.data['genre'], 'Rock')

    def test_create_artist(self):
        url = reverse('artist-list')
        data = {'name': 'New Artist', 'genre': 'Pop'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 2)
        self.assertEqual(Artist.objects.last().name, 'New Artist')

    def test_update_artist(self):
        url = reverse('artist-detail', args=[self.artist.id])
        data = {'name': 'Updated Artist', 'genre': 'Alternative'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.artist.refresh_from_db()
        self.assertEqual(self.artist.name, 'Updated Artist')
        self.assertEqual(self.artist.genre, 'Alternative')

    def test_delete_artist(self):
        url = reverse('artist-detail', args=[self.artist.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Artist.objects.count(), 0)
