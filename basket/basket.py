class Basket(object):
    """
    A base Basket class, providing some default behaviors that can be inherited or
    overrided, as necessary
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
        product_id = product.id

        if product_id not in self.basket:
            self.basket[product_id] = {"price": str(product.price), "qty": int(qty)}
        self.session.modified = True
        print(self.basket)

    def __len__(self):
        """
        Get the basket data and get the quantity of items
        """
        return sum([item["qty"] for item in self.basket.values()])
