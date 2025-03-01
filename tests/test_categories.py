## This test was written by ChatGPT

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from merchexchangeapi.models import Category

class CategoryIntegrationTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(label='Test Category')

    def test_get_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['label'], 'Test Category')

    def test_get_single_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'Test Category')

    def test_create_category(self):
        url = reverse('category-list')
        data = {'label': 'New Category'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.last().label, 'New Category')

    def test_update_category(self):
        url = reverse('category-detail', args=[self.category.id])
        data = {'label': 'Updated Category'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.label, 'Updated Category')

    def test_delete_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)
