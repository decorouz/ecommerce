from unicodedata import category
from django.test import TestCase
from store.models import Product, Author, Category
from django.contrib.auth.models import User


class TestAuthorsModel(TestCase):
    def setUp(self):
        self.data1 = Author.objects.create(first_name="james", last_name="peter", slug="peter-james")

    def test_authors_model_entry(self):
        """
        Test Author model data insertion/types/fields attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Author))
        self.assertEqual(str(data), "james, peter")


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name="python", slug="python")

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/fields attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), "python")


class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name="python", slug="python")
        User.objects.create(username="elon")
        Author.objects.create(first_name="elon")
        self.data1 = Product.objects.create(
            title="Great django",
            slug="great-django",
            price="20.00",
            image="python",
            created_by_id=1,
            author_id=1,
            category_id=1,
        )

    def test_product_model_entry(self):
        """
        Test Product model data insertion/types/fields/attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), "Great django")
