## This test was written by ChatGPT

from rest_framework.test import APITestCase
from rest_framework import status
from merchexchangeapi.models import Category
from rest_framework.reverse import reverse

class CategoryViewSetTest(APITestCase):

    def setUp(self):
        self.category_data = {
            "label": "Test Category",
        }
        self.category = Category.objects.create(**self.category_data)

    def test_create_category(self):
        url = reverse('category-list')  # Assuming the URL name is 'category-list'
        data = {
            "label": "New Category",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["label"], "New Category")

    def test_list_categories(self):
        url = reverse('category-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should be 1 since we added one category in setUp
        self.assertEqual(response.data[0]["label"], self.category.label)

    def test_retrieve_category(self):
        url = reverse('category-detail', args=[self.category.id])  # Assuming URL name is 'category-detail'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["label"], self.category.label)

    def test_update_category(self):
        url = reverse('category-detail', args=[self.category.id])
        data = {
            "label": "Updated Category",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()  # Refresh the instance from the database
        self.assertEqual(self.category.label, "Updated Category")

    def test_delete_category(self):
        url = reverse('category-detail', args=[self.category.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure category was deleted
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=self.category.id)
    
    def test_category_not_found(self):
        url = reverse('category-detail', args=[9999])  # Non-existing ID
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Category matching query does not exist.')
