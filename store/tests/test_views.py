# from unittest import skip

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Author, Category, Product
from store.views import all_products


class TestViewResponse(TestCase):
    def setUp(self) -> None:
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name="python", slug="python")
        User.objects.create(username="elon")
        Author.objects.create(first_name="elon", last_name="musk", slug="musk-elon")
        Product.objects.create(
            title="Great django",
            slug="great-django",
            price="20.00",
            image="python",
            created_by_id=1,
            author_id=1,
            category_id=1,
        )

    def test_url_allowed_host(self):
        """Test Allowed host"""
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """Test Product response status"""

        response = self.c.get(reverse("store:product_detail", args=["great-django"]))
        self.assertEqual(response.status_code, 200)

    def test_categories_detail_url(self):
        """Test Category response status"""
        response = self.c.get(reverse("store:category_list", args=["python"]))
        self.assertEqual(response.status_code, 200)

    def test_author_detail_url(self):
        """Test Author response status"""
        response = self.c.get(reverse("store:author_detail", args=["musk-elon"]))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        request = HttpRequest()
        response = all_products(request)
        html = response.content.decode("utf8")

        self.assertIn("<title>Home</title>", html)
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):

        request = self.factory.get("/product/zero-to-hero")
        response = all_products(request)
        html = response.content.decode("utf8")
        self.assertIn("<title>Home</title>", html)
        self.assertTrue(html.startswith("\n<!DOCTYPE html>"))
        self.assertEqual(response.status_code, 200)
