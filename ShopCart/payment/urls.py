from django.urls import path

from .views import payment_success, payment_fail, shipping, checkout, complete_order
from .webhooks import stripe_webhook

app_name = 'payment'

urlpatterns = [
    path('payment-success/', payment_success, name='payment-success'),
    path('payment-fail/', payment_fail, name='payment-fail'),
    path('shipping/', shipping, name='shipping'),
    path('checkout/', checkout, name='checkout'),
    path('complete-order/', complete_order, name='complete-order'),
    path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),

]
