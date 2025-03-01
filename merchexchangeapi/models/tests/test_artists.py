## This test was written by ChatGPT

from django.test import TestCase
from merchexchangeapi.models import Artist

class ArtistModelTest(TestCase):

    def test_create_artist(self):
        artist = Artist.objects.create(name="Test Artist", genre="Rock")
        self.assertEqual(artist.name, "Test Artist")
        self.assertEqual(artist.genre, "Rock")
        self.assertIsInstance(artist, Artist)

    def test_artist_str_method(self):
        artist = Artist.objects.create(name="Test Artist", genre="Pop")
        self.assertEqual(str(artist), "Test Artist")
