from decimal import Decimal
from itertools import product
from store.models import Product


class Basket(object):
    """
    A base Basket class, providing some default behaviors that can be inherited or overrided, as necessary
    """

    def __init__(self, request) -> None:
        self.session = request.session
        basket = self.session.get("skey")
        if not basket:
            basket = self.session["skey"] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Add product to cart and update it quantity
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        else:
            self.basket[product_id] = {"price": str(product.price), "qty": qty}

        self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        """
        Get the basket data and get the quantity of items
        """
        return sum([item["qty"] for item in self.basket.values()])

    def __iter__(self):
        """Collect the product id in the session data to query
        the database and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def get_total_price(self):
        return sum([Decimal(item["price"]) * item["qty"] for item in self.basket.values()])

    def delete(self, product):
        """
        Delete a selected product from session data
        """
        product_id = str(product)
        print(product_id)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self, product, qty):
        """
        update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        self.save()
