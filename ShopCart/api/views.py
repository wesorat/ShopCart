from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from recommend.models import Review
from shop.models import Product

from .serializers import ProductSerializer, ProductDetailSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly

class ProductListApiView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly,]
    queryset = Product.objects.select_related('category').order_by('id')
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAdminOrReadOnly,]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'


class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        existing_review = Review.objects.filter(product=product,
                                                created_by=self.request.user).exists()
        if existing_review:
            raise ValidationError('You have already review of this product')

        serializer.save(created_by=self.request.user, product=product)


