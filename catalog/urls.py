from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import ProductsListView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductUpdateView, ContactViews

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductsListView.as_view(), name="product_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("contacts/", ContactViews.as_view(), name="contacts"),
    # path("product/<int:pk>/", views.product, name="product"),
    # path("contacts/", views.contacts, name="contacts"),
]
