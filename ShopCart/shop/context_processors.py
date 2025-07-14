from .models import Category


def categories(request):
    #categories = Category.objects.all()
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}