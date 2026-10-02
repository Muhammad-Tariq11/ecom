from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryUpdateView,
    ProductListCreateView,
    ProductUpdateView,
    ProductSKUListCreateView,
    VariantListCreateView,
    VariantUpdateView,
    SKUListView,
    SKUUpdateView,
)

urlpatterns = [
    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list-create",
    ),
    path(
        "categories/<int:pk>/",
        CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "products/",
        ProductListCreateView.as_view(),
        name="product-list-create",
    ),
    path(
        "products/<int:pk>/",
        ProductUpdateView.as_view(),
        name="product-update",
    ),
    path(
        "variants/",
        VariantListCreateView.as_view(),
        name="variant-list-create",
    ),
    path(
        "variants/<int:pk>/",
        VariantUpdateView.as_view(),
        name="variant-update",
    ),
    path(
        "skus/",
        SKUListView.as_view(),
        name="sku-list",
    ),
    path(
        "skus/<int:pk>/",
        SKUUpdateView.as_view(),
        name="sku-update",
    ),

    path(
        "products/<int:pk>/skus/", 
        ProductSKUListCreateView.as_view(), 
        name="product-sku-list-create"
        
    ),
]

