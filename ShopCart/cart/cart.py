from decimal import Decimal

from shop.models import ProductProxy


class Cart:

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if not cart:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def __len__(self):
        return sum(pr['count'] for pr in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for pr in cart.values():
            pr['price'] = Decimal(pr['price'])
            pr['total'] = pr['price'] * pr['count']
            yield pr

    def add(self, product, count):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'count': count, 'price': str(product.get_discounted_price())}
        else:
            self.cart[product_id]['count'] = count
        self.session.modified = True

    def remove(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def update(self, product, count):
        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]['count'] = count
            self.session.modified = True

    def get_subtotal_price(self):
        sm = sum(Decimal(pr['price']) * pr['count'] for pr in self.cart.values())
        return sm



