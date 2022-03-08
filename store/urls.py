from django.urls import path

from . import views

app_name = "store"
urlpatterns = [
    path("", views.all_products, name="all_products"),
    path("product/<slug:slug>", views.product_detail, name="product_detail"),
    path("shop/<slug:category_slug>", views.category_list, name="category_list"),
    path("author/<slug:slug>", views.author_detail, name="author_detail"),
]
