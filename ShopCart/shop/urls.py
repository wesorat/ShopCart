from django.urls import path
from .views import product_detail_view, products_view, category_list, search_products


app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('search/<slug:slug>/', category_list, name='category-list'),
    path('search_products/', search_products, name='search-products'),
    path('<slug:slug>/', product_detail_view, name='product-detail'),

]