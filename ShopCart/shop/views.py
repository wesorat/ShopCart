from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Category, ProductProxy
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
def products_view(request):
    products = ProductProxy.objects.all()
    return render(request, 'shop/products.html', {'products': products})


def product_detail_view(request, slug):
    product = get_object_or_404(
        ProductProxy.objects.select_related('category'), slug=slug)

    if request.method == 'POST':
        if request.user.is_authenticated:
            if product.reviews.filter(created_by=request.user).exists():
                ...
            else:
                rating = request.POST.get('rating', 3)
                content = request.POST.get('content', '')
                if content:
                    product.reviews.create(
                        rating=rating, content=content, created_by=request.user, product=product)
                    return redirect(request.path)

    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = ProductProxy.objects.select_related('category').filter(category__in=category.get_all_related_category())
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category_list.html', context=context)


def search_products(request):
    query = request.GET.get('q')
    print(query)
    products = ProductProxy.objects.filter(title__icontains=query).distinct()
    context = {
        'products': products,

    }
    return render(request, 'shop/products.html', context)

