from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Category, Product, Variant, SKU
from .serializers import CategorySerializer, ProductSerializer, VariantSerializer, SKUSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class CategoryUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        return super().get_serializer(*args, **kwargs)

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class ProductUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        return super().get_serializer(*args, **kwargs)

class ProductSKUListCreateView(generics.ListCreateAPIView):
    serializer_class = SKUSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return SKU.objects.filter(variant__product_id=self.kwargs["pk"])

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs["pk"])
        variant_id = self.request.data.get("variant")

        variant = get_object_or_404(
            Variant,
            pk=variant_id,
            product=product
        )

        serializer.save(variant=variant)

class VariantListCreateView(generics.ListCreateAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = [IsAdminUser]


class VariantUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = [IsAdminUser]

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        return super().get_serializer(*args, **kwargs)

class SKUListView(generics.ListAPIView):
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer
    permission_classes = [IsAdminUser]


class SKUUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer
    permission_classes = [IsAdminUser]

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        return super().get_serializer(*args, **kwargs)