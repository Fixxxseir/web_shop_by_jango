from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (ProductHomeView, ProductContactsView, ProductListView,
                           ProductDetailView, ProductCreateView)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductHomeView.as_view(), name="home"),
    path("catalog/contacts/", ProductContactsView.as_view(), name="contacts"),
    path("catalog/product_list/", ProductListView.as_view(), name="product_list"),
    path("catalog/product/<slug:product_slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("catalog/add_product/", ProductCreateView.as_view(), name="add_product"),
]
