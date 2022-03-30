import pytest
from django.urls import reverse


def test_category_str(product_category):
    assert product_category.__str__() == "django"
