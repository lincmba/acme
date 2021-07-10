from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Products AppConfig class
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acme.products'
    verbose_name = "products"
