from django.urls import path, include
from .views import cart_add, cart_remove, cart_update, cart_view

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/', cart_add, name='add_to_cart'),
    path('remove/', cart_remove, name='cart_remove'),
    path('update/', cart_update, name='cart_update'),


]