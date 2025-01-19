from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


class ProductServices:
    @staticmethod
    def get_products_from_cache():
        """Получает данные из кеша, если кеша нет то получает данные из бд и добавляет в кеш"""

        if not CACHE_ENABLED:
            return Product.objects.all()

        key = "product_list"
        products = cache.get(key)

        if products is not None:
            return products

        products = Product.objects.all()
        cache.set(key, products)

        return products

    @staticmethod
    def get_product_by_category(category_id):

        product_by_category = Product.objects.filter(category_id=category_id)

        if not product_by_category:
            product_by_category = None

        return product_by_category
