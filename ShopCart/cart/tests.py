import json

from django.contrib.sessions.middleware import SessionMiddleware

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from .cart import Cart

from shop.models import Category, ProductProxy

from .views import cart_add, cart_remove, cart_update, cart_view

class CartViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory().get(reverse('cart:cart'))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_view(self):
        request = self.factory
        responce = cart_view(request)
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(self.client.get(reverse('cart:cart')), 'cart/cart_view.html')


class CartAddViewTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('cart:add_to_cart'), {
            'product_id': self.product.id,
            'count': 3,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_add(self):
        request = self.factory
        response = cart_add(request)
        cart = Cart(request)

        self.assertEqual(response.status_code, 302)
        self.assertIn(str(self.product.id), cart.cart )
        self.assertEqual(cart.cart[str(self.product.id)]['count'], 3)

class CartDeleteViewTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('cart:cart_remove'), {
            'product_id': self.product.id,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_delete(self):
        request = self.factory
        response = cart_remove(request)
        cart = Cart(request)

        self.assertEqual(response.status_code, 302)
        self.assertNotIn(str(self.product.id), cart.cart)


class CartUpdateViewTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('cart:add_to_cart'), {
            'product_id': self.product.id,
            'count': 2,
        })
        self.factory = RequestFactory().post(reverse('cart:cart_update'), {
            'product_id': self.product.id,
            'count': 3,
        })
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()

    def test_cart_update(self):
        request = self.factory
        response = cart_add(request)
        response = cart_update(request)
        cart = Cart(request)

        self.assertEqual(response.status_code, 302)
        self.assertIn(str(self.product.id), cart.cart)
        self.assertEqual(cart.cart[str(self.product.id)]['count'], 3)