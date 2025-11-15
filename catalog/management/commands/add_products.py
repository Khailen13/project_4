from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add products to the database"

    def handle(self, *args, **kwargs):
        # Удаление существующих записей
        Category.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(name="Овощи")

        products = [
            {"name": "Картофель", "category": category, "price": "50"},
            {"name": "Морковь", "category": category, "price": "100"},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully added book: {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Book already exists: {product.name}"))
