from rest_framework import serializers
from .models import Category, Product, Variant, SKU


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "parent",
            "name",
            "slug",
            "active_status",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        category = self.instance

        if category is not None and "parent" in attrs:
            new_parent = attrs["parent"]

            if new_parent is not None:
                if new_parent.pk == category.pk:
                    raise serializers.ValidationError({
                        "parent": "A category cannot be its own parent."
                    })

                ancestor = new_parent

                while ancestor is not None:
                    if ancestor.pk == category.pk:
                        raise serializers.ValidationError({
                            "parent": "A category cannot become its own ancestor."
                        })

                    ancestor = ancestor.parent

        return attrs


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "slug",
            "description",
            "status",
            "specifications",
            "created_at",
            "updated_at",
        ]

    def validate_specifications(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Specifications must be a JSON object."
            )
        return value

    def validate(self, attrs):
        status = attrs.get(
            "status",
            getattr(self.instance, "status", None)
        )

        if status == "published" and self.instance is not None:
            has_sellable_sku = self.instance.variants.filter(
                skus__active_status=True,
                skus__stock_quantity__gt=0
            ).exists()

            if not has_sellable_sku:
                raise serializers.ValidationError(
                    "A published product must have at least one active SKU with available stock."
                )

        return attrs

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            "id",
            "product",
            "option_values",
            "created_at",
            "updated_at",
        ]

class SKUSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = [
            "id",
            "variant",
            "sku_code",
            "price",
            "stock_quantity",
            "active_status",
            "created_at",
            "updated_at",
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Price cannot be negative."
            )
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Stock quantity cannot be negative."
            )
        return value