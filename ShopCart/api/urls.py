from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from .views import ProductListApiView, ProductDetailAPIView, ReviewCreateView

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title='ShopCart API',
        default_version='v1',
        description='Some description',
        terms_of_service='https://examples.com/terms/',
        contact=openapi.Contact(email='projectucheb@gmail.com'),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
)


urlpatterns = [
    path("products/", ProductListApiView.as_view(), name='products'),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name='product-detail'),
    path('reviews/create/', ReviewCreateView.as_view(), name='reviews-create'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
