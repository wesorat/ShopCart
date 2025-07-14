import random
import string

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Категория', max_length=250, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               related_name='children', blank=True, null=True)
    slug = models.SlugField('URL', max_length=250, unique=True, null=False,
                            editable=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        '''Возвращает полный путь к категории Родитель > Дочерняя'''
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    @staticmethod
    def _rand_slug():
        '''update не запускается в коде(вроде)
        Генерация 5 символьной строки для уникальности slug
        '''
        res = []
        for i in range(5):
            res.append(random.choice(string.ascii_lowercase + string.digits))

        return ''.join(res)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self._rand_slug() + ' ' + self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category-list", args=[str(self.slug)])

    def get_all_related_category(self):
        children = [self]
        for child in self.children.all():
            children.extend(child.get_all_related_category())
        return children






class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField("Название", max_length=250)
    brand = models.CharField("Бренд", max_length=250)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField('URL', max_length=250)
    '''update добавить индекс для фильтрации полей db_index=True'''
    price = models.DecimalField(
        "Цена", max_digits=7, decimal_places=2, default=100.00,
        validators=[MinValueValidator(1)])
    image = models.ImageField(
        "Изображение", upload_to='images/products/%Y/%m/%d', default='images/products/default.png')
    available = models.BooleanField("Наличие", default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product-detail", args=[str(self.slug)])

    def get_discounted_price(self):
        discounted_price = self.price - (self.price * self.discount / 100)
        return round(discounted_price, 2)

    @property
    def full_image_url(self):
        return self.image.url if self.image else ''

    @staticmethod
    def _rand_slug():
        '''update не запускается в коде(вроде)
        Генерация 5 символьной строки для уникальности slug
        '''
        res = []
        for i in range(5):
            res.append(random.choice(string.ascii_lowercase + string.digits))

        return ''.join(res)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self._rand_slug() + ' ' + self.title)
        super().save(*args, **kwargs)

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)


class ProductProxy(Product):
    objects = ProductManager()

    class Meta:
        proxy = True

