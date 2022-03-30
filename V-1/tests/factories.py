from ast import Store

import factory
from faker import Faker
from store.models import Category

fake = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "django"
    slug = "django"
