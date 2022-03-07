from django.contrib import admin
from .models import Author, Category, Product

# Register your models here.


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")
    prepopulated_fields = {"slug": ("last_name", "first_name")}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "slug", "price", "in_stock", "created", "updated"]

    list_filter = ["in_stock", "is_active"]
    list_editable = ["in_stock", "price"]
    prepopulated_fields = {"slug": ("title", "author")}
