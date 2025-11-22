from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_products_from_cache():
    """Получает данные всех продуктов из кэша или из базы данных."""

    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products


def get_category_products(category_id):
    """Возвращает список всех продуктов входящей категории"""

    category_products = Product.objects.filter(category_id=category_id)
    return category_products
