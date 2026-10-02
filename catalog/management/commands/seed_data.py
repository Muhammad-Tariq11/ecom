from decimal import Decimal
from django.core.management.base import BaseCommand
from catalog.models import Category, Product, Variant, SKU

class Command(BaseCommand):
    help = "Create reproducible seed data for the e-commerce catalog."

    def handle(self, *args, **options):

        
        # Categories
        
        laptops, _ = Category.objects.get_or_create(
            slug="laptops",
            defaults={
                "name": "Laptops",
                "parent": None,
                "active_status": True,
            },
        )

        dell, _ = Category.objects.get_or_create(
            slug="dell",
            defaults={
                "name": "Dell",
                "parent": laptops,
                "active_status": True,
            },
        )

        hp, _ = Category.objects.get_or_create(
            slug="hp",
            defaults={
                "name": "HP",
                "parent": laptops,
                "active_status": True,
            },
        )

        lenovo, _ = Category.objects.get_or_create(
            slug="lenovo",
            defaults={
                "name": "Lenovo",
                "parent": laptops,
                "active_status": True,
            },
        )

        pc_components, _ = Category.objects.get_or_create(
            slug="pc-components",
            defaults={
                "name": "PC Components",
                "parent": None,
                "active_status": True,
            },
        )

        ram, _ = Category.objects.get_or_create(
            slug="ram",
            defaults={
                "name": "RAM",
                "parent": pc_components,
                "active_status": True,
            },
        )

        graphics_cards, _ = Category.objects.get_or_create(
            slug="graphics-cards",
            defaults={
                "name": "Graphics Cards",
                "parent": pc_components,
                "active_status": True,
            },
        )

        
        # Product 1: Dell Inspiron 15
        # Multiple variants
        

        dell_inspiron, _ = Product.objects.get_or_create(
            slug="dell-inspiron-15",
            defaults={
                "category": dell,
                "name": "Dell Inspiron 15",
                "description": "15-inch Dell laptop for everyday computing.",
                "status": "published",
                "specifications": {
                    "processor": "Intel Core i5",
                    "screen": "15.6-inch",
                    "storage": "512GB SSD",
                },
            },
        )

        dell_black_16, _ = Variant.objects.get_or_create(
            product=dell_inspiron,
            option_values={
                "color": "Black",
                "ram": "16GB",
            },
        )

        dell_silver_16, _ = Variant.objects.get_or_create(
            product=dell_inspiron,
            option_values={
                "color": "Silver",
                "ram": "16GB",
            },
        )

        dell_black_32, _ = Variant.objects.get_or_create(
            product=dell_inspiron,
            option_values={
                "color": "Black",
                "ram": "32GB",
            },
        )

        SKU.objects.get_or_create(
            sku_code="DELL-INSP-BLK-16",
            defaults={
                "variant": dell_black_16,
                "price": Decimal("145000.00"),
                "stock_quantity": 10,
                "active_status": True,
            },
        )

        SKU.objects.get_or_create(
            sku_code="DELL-INSP-SLV-16",
            defaults={
                "variant": dell_silver_16,
                "price": Decimal("147000.00"),
                "stock_quantity": 8,
                "active_status": True,
            },
        )

        SKU.objects.get_or_create(
            sku_code="DELL-INSP-BLK-32",
            defaults={
                "variant": dell_black_32,
                "price": Decimal("160000.00"),
                "stock_quantity": 5,
                "active_status": True,
            },
        )

        # Silver + 32GB is intentionally unavailable.
        # No Variant or SKU is created for this combination.

        
        # Product 2: HP Victus 15
        

        hp_victus, _ = Product.objects.get_or_create(
            slug="hp-victus-15",
            defaults={
                "category": hp,
                "name": "HP Victus 15",
                "description":
                "15-inch HP gaming laptop for gaming and everyday performance.",
                "status": "published",
                "specifications": {
                    "processor": "AMD Ryzen 5",
                    "screen": "15.6-inch",
                    "storage": "512GB SSD",
                },
            },
        )

        hp_variant, _ = Variant.objects.get_or_create(
            product=hp_victus,
            option_values={
                "color": "Silver",
                "ram": "16GB",
            },
        )

        SKU.objects.get_or_create(
            sku_code="HP-VICTUS15-SLV-16",
            defaults={
                "variant": hp_variant,
                "price": Decimal("200000.00"),
                "stock_quantity": 7,
                "active_status": True,
            },
        )

        
        # Product 3: Corsair Vengeance 16GB
        

        corsair_ram, _ = Product.objects.get_or_create(
            slug="corsair-vengeance-16gb",
            defaults={
                "category": ram,
                "name": "Corsair Vengeance 16GB",
                "description": "16GB DDR4 desktop memory module.",
                "status": "published",
                "specifications": {
                    "memory_type": "DDR4",
                    "capacity": "16GB",
                },
            },
        )

        corsair_variant, _ = Variant.objects.get_or_create(
            product=corsair_ram,
            option_values={
                "capacity": "16GB",
            },
        )

        SKU.objects.get_or_create(
            sku_code="CORSAIR-VEN-16",
            defaults={
                "variant": corsair_variant,
                "price": Decimal("12000.00"),
                "stock_quantity": 20,
                "active_status": True,
            },
        )

        
        # Product 4: NVIDIA GeForce RTX 4060
        

        rtx_4060, _ = Product.objects.get_or_create(
            slug="nvidia-geforce-rtx-4060",
            defaults={
                "category": graphics_cards,
                "name": "NVIDIA GeForce RTX 4060",
                "description":
                "Graphics card for desktop gaming and GPU workloads.",
                "status": "published",
                "specifications": {
                    "memory": "8GB",
                    "memory_type": "GDDR6",
                },
            },
        )

        rtx_variant, _ = Variant.objects.get_or_create(
            product=rtx_4060,
            option_values={
                "memory": "8GB",
            },
        )

        SKU.objects.get_or_create(
            sku_code="NVIDIA-RTX4060-8GB",
            defaults={
                "variant": rtx_variant,
                "price": Decimal("95000.00"),
                "stock_quantity": 6,
                "active_status": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS("Seed data created successfully."))