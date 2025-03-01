## This test was written by ChatGPT

from django.test import TestCase
from merchexchangeapi.models import Category

class CategoryModelTest(TestCase):

    def test_create_category(self):
        category = Category.objects.create(label="Test Category")
        self.assertEqual(category.label, "Test Category")
        self.assertIsInstance(category, Category)

    def test_category_str_method(self):
        category = Category.objects.create(label="Test Category")
        self.assertEqual(str(category), "Test Category")
