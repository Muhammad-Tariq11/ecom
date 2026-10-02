from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category, Product, Variant, SKU

class ProductAndSKUTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Laptops",
            slug="laptops",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Dell Inspiron 15",
            slug="dell-inspiron-15",
            status="draft",
        )

        self.variant = Variant.objects.create(
            product=self.product,
            option_values={
                "color": "Black",
                "ram": "16GB",
            },
        )

    def test_product_creation_with_required_fields(self):
        product = Product.objects.create(
            category=self.category,
            name="HP Pavilion 15",
            slug="hp-pavilion-15",
            status="draft",
        )

        self.assertEqual(product.name, "HP Pavilion 15")
        self.assertEqual(product.slug, "hp-pavilion-15")

    def test_sku_creation_with_required_fields(self):
        sku = SKU.objects.create(
            variant=self.variant,
            sku_code="DELL-INSP-BLK-16",
            price=Decimal("80000.00"),
            stock_quantity=5,
            active_status=True,
        )

        self.assertEqual(sku.sku_code, "DELL-INSP-BLK-16")
        self.assertEqual(sku.stock_quantity, 5)

    def test_duplicate_product_slug_is_rejected(self):
        Product.objects.create(
            category=self.category,
            name="Dell Vostro 15",
            slug="duplicate-laptop",
            status="draft",
        )

        duplicate = Product(
            category=self.category,
            name="HP Pavilion 15",
            slug="duplicate-laptop",
            status="draft",
        )

        with self.assertRaises(ValidationError):
            duplicate.validate_unique()

    def test_duplicate_sku_code_is_rejected(self):
        SKU.objects.create(
            variant=self.variant,
            sku_code="DELL-DUPLICATE-16",
            price=Decimal("80000.00"),
            stock_quantity=5,
            active_status=True,
        )

        duplicate = SKU(
            variant=self.variant,
            sku_code="DELL-DUPLICATE-16",
            price=Decimal("85000.00"),
            stock_quantity=10,
            active_status=True,
        )

        with self.assertRaises(ValidationError):
            duplicate.validate_unique()

    def test_negative_stock_is_rejected(self):
        sku = SKU(
            variant=self.variant,
            sku_code="DELL-NEG-STOCK",
            price=Decimal("80000.00"),
            stock_quantity=-1,
            active_status=True,
        )

        with self.assertRaises(ValidationError):
            sku.full_clean()

    def test_negative_price_is_rejected(self):
        sku = SKU(
            variant=self.variant,
            sku_code="DELL-NEG-PRICE",
            price=Decimal("-1000.00"),
            stock_quantity=5,
            active_status=True,
        )

        with self.assertRaises(ValidationError):
            sku.full_clean()


class CategoryHierarchyTests(TestCase):

    def test_category_can_have_a_parent(self):
        parent = Category.objects.create(
            name="Computers",
            slug="computers",
        )

        child = Category.objects.create(
            name="Laptops",
            slug="laptops",
            parent=parent,
        )

        self.assertEqual(child.parent, parent)

    def test_category_cannot_be_its_own_parent(self):
        category = Category.objects.create(
            name="Laptops",
            slug="laptops",
        )

        category.parent = category

        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_category_cannot_become_its_own_ancestor(self):
        parent = Category.objects.create(
            name="Computers",
            slug="computers",
        )

        child = Category.objects.create(
            name="Laptops",
            slug="laptops",
            parent=parent,
        )

        grandchild = Category.objects.create(
            name="Gaming Laptops",
            slug="gaming-laptops",
            parent=child,
        )

        parent.parent = grandchild

        with self.assertRaises(ValidationError):
            parent.full_clean()


class VariantAndSKUTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Laptops",
            slug="laptops",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Dell Inspiron 15",
            slug="dell-inspiron-15",
            status="draft",
        )

    def test_valid_variant_and_sku_creation(self):
        variant = Variant.objects.create(
            product=self.product,
            option_values={
                "color": "Black",
                "ram": "16GB",
            },
        )

        sku = SKU.objects.create(
            variant=variant,
            sku_code="DELL-INSP-BLK-16",
            price=Decimal("80000.00"),
            stock_quantity=5,
            active_status=True,
        )

        self.assertEqual(variant.product, self.product)
        self.assertEqual(sku.variant, variant)
        self.assertEqual(sku.stock_quantity, 5)

    def test_duplicate_variant_combination_is_rejected(self):
        Variant.objects.create(
            product=self.product,
            option_values={
                "color": "Black",
                "ram": "16GB",
            },
        )

        duplicate = Variant(
            product=self.product,
            option_values={
                "color": "Black",
                "ram": "16GB",
            },
        )

        with self.assertRaises(IntegrityError):
            duplicate.save()


class AuthorizationTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_anonymous_user_cannot_create_category(self):
        response = self.client.post(
            "/api/v1/admin/categories/",
            {
                "name": "Laptops",
                "slug": "laptops",
                "active_status": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_create_product(self):
        response = self.client.post(
            "/api/v1/admin/products/",
            {
                "category": 1,
                "name": "Dell Inspiron 15",
                "slug": "dell-inspiron-15",
                "status": "draft",
                "specifications": {},
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_create_variant(self):
        response = self.client.post(
            "/api/v1/admin/variants/",
            {
                "product": 1,
                "option_values": {
                    "color": "Black",
                    "ram": "16GB",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_cannot_create_sku(self):
        response = self.client.post(
            "/api/v1/admin/products/1/skus/",
            {
                "variant": 1,
                "sku_code": "DELL-INSP-BLK-16",
                "price": "80000.00",
                "stock_quantity": 5,
                "active_status": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)