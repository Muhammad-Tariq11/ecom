from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        from django.core.exceptions import ValidationError

        super().clean()

        # Prevent a category from becoming its own ancestor.
        if not self.parent_id:
            return

        if self.pk and self.parent_id == self.pk:
            raise ValidationError({
                "parent": "A category cannot be its own parent."
            })

        ancestor = self.parent

        while ancestor is not None:
            if self.pk and ancestor.pk == self.pk:
                raise ValidationError({
                    "parent": "A category cannot become its own ancestor."
                })

            ancestor = ancestor.parent


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20,choices=[("draft", "Draft"),("published", "Published"),("archived", "Archived"),],
    default="draft",
)
    specifications = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Variant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )
    option_values = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - Variant {self.id}"

    class Meta:
        constraints = [
            # Prevent duplicate variant options for the same product.
            models.UniqueConstraint(
                fields=["product", "option_values"],
                name="unique_product_variant_options"
            ),
        ]


class SKU(models.Model):
    variant = models.ForeignKey(
        Variant,
        on_delete=models.PROTECT,
        related_name="skus"
    )
    sku_code = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    active_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku_code

    class Meta:
        constraints = [
            # Prevent negative stock and negative prices.
            models.CheckConstraint(
                condition=models.Q(stock_quantity__gte=0),
                name="sku_stock_non_negative"
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="sku_price_non_negative"
            ),
        ]


class Asset(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="assets"
    )
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="assets"
    )
    storage_key = models.CharField(max_length=500)
    role = models.CharField(max_length=50)
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.IntegerField(default=0)

    def __str__(self):
        return self.storage_key

    class Meta:
        constraints = [
            # Each asset must belong to exactly one parent: product or variant.
            models.CheckConstraint(
                condition=(
                    models.Q(product__isnull=False, variant__isnull=True)
                    | models.Q(product__isnull=True, variant__isnull=False)
                ),
                name="asset_exactly_one_parent"
            ),
        ]

class Cart(models.Model):
    user = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    sku = models.ForeignKey(
        SKU,
        on_delete=models.PROTECT,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.sku.sku_code} x {self.quantity}"

    class Meta:
            constraints = [
                # Cart item quantity must be greater than zero.
                models.CheckConstraint(
                    condition=models.Q(quantity__gt=0),
                    name="cart_item_quantity_positive"
                ),
            ]


class Order(models.Model):
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.PROTECT,
        related_name="orders"
    )
    shipping_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    sku = models.ForeignKey(
        SKU,
        on_delete=models.PROTECT,
        related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.sku.sku_code} x {self.quantity}"

    class Meta:
            constraints = [
                # Order item quantity must be greater than zero.
                models.CheckConstraint(
                    condition=models.Q(quantity__gt=0),
                    name="order_item_quantity_positive"
                ),
            ]