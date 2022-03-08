from django.shortcuts import get_object_or_404, render

from .models import Author, Category, Product

# Create your views here.


def categories(request):
    return {"categories": Category.objects.all()}


def all_products(request):
    products = Product.objects.all()

    context = {"products": products}
    return render(request, "store/home.html", context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)

    return render(request, "store/products/detail.html", {"product": product})


def category_list(request, category_slug):
    category = None
    products = Product.objects.filter(in_stock=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {"category": category, "products": products}

    return render(request, "store/products/category.html", context)


def author_detail(request, slug):
    author = get_object_or_404(Author, slug=slug)

    return render(request, "store/products/author_detail.html", {"author": author})
