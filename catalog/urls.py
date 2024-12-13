from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, catalog, product_detail, add_product

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts"),
    path("catalog/", catalog, name="catalog"),
    path("product/<slug:product_slug>/", product_detail, name="product_detail"),
    path("add_product/", add_product, name="add_product"),
]
