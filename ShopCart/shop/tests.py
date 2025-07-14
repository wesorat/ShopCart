from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Category, Product, ProductProxy


class ProductViewTest(TestCase):
    def test_get_products(self):
        small_gif = b''

        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='django')
        product_1 = ProductProxy.objects.create(title='Product 1', category=category, image=uploaded)
        product_2 = ProductProxy.objects.create(title='Product 2', category=category, image=uploaded)

        response = self.client.get(reverse('shop:products'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products'].count(), 2)
        self.assertEqual(list(response.context['products']), [product_2, product_1])
        self.assertContains(response, product_1)
        self.assertContains(response, product_2)


class ProductDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        small_gif = b''
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image5/gif')
        category = Category.objects.create(name='Category 1')
        product = ProductProxy.objects.create(
            title='Product 1', category=category, slug='product-1', image=uploaded)
        response = self.client.get(
            reverse('shop:product-detail', args=['product-1']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertEqual(response.context['product'].slug, product.slug)


class CategoryListViewTest(TestCase):
    def setUp(self):
        small_gif = b''
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        self.product = ProductProxy.objects.create(
            title='Test Product', slug='test-product', category=self.category, image=uploaded)

    def test_get_category_and_products(self):

        response = self.client.get(
            reverse('shop:category-list', args=[self.category.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/category_list.html')
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)