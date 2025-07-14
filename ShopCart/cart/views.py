from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseRedirect

from shop.models import ProductProxy
from .cart import Cart

def cart_view(request):
    cart = Cart(request)
    context = {
        'cart': cart,
    }

    return render(request, 'cart/cart_view.html', context=context)

def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_count = int(request.POST.get('count'))

        product = get_object_or_404(ProductProxy, id=product_id)

        cart.add(product=product, count=product_count)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def cart_remove(request):
    cart = Cart(request)
    if request.method == 'POST':

        product_id = request.POST.get('product_id')
        cart.remove(product=product_id)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_update(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_count = int(request.POST.get('count'))

        cart.update(product=product_id, count=product_count)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
