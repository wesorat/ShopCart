from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

import stripe


from cart.cart import Cart

from .forms import ShippingAddressForm
from .models import Order, OrderItem, ShippingAddress

from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def payment_success(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'payment/payment-success.html')


def payment_fail(request):
    return render(request, 'payment/payment-fail.html')


@login_required(login_url='account:login-user')
def shipping(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None

    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:dashboard')

    form = ShippingAddressForm(instance=shipping_address)
    context = {
        'form': form,

    }
    return render(request, 'payment/shipping.html', context=context)


@login_required(login_url='account:login-user')
def checkout(request):

    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            shipping_address = None

        if shipping_address:

            context = {
                'shipping_address': shipping_address,
            }

            return render(request, 'payment/checkout.html', context=context)

    return render(request, 'payment/checkout.html')


@login_required(login_url='account:login-user')
def complete_order(request):
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')

        cart = Cart(request)
        total_price = cart.get_subtotal_price()

        if payment_type == 'stripe-payment':
            shipping_address, _ = ShippingAddress.objects.get_or_create(
                user=request.user,
                defaults={
                    'full_name': full_name,
                    'email': email,
                    'street_address': street_address,
                    'apartment_address': apartment_address,
                    'country': country,
                    'zip_code': zip_code,
                }
            )

            session_data = {
                'mode': 'payment',
                'success_url': request.build_absolute_uri(reverse('payment:payment-success')),
                'cancel_url': request.build_absolute_uri(reverse('payment:payment-fail')),
                'line_items': [],
                'customer_email': email,
            }

            order = Order.objects.create(user=request.user, shipping_address=shipping_address,
                                         amount=total_price)
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['count'], user=request.user)
                session_data['line_items'].append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item['price'] * Decimal(100)),
                        'product_data': {
                            'name': item['product'],
                        },
                    },
                    'quantity': item['count'],
                })
            session_data['client_reference_id'] = order.id
            session = stripe.checkout.Session.create(**session_data)
            return redirect(session.url, code=303)
    return redirect('payment:payment-fail')
