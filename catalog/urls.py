from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.main, name="main"),
    path("product/<int:pk>/", views.product, name="product"),
    path("contacts/", views.contacts, name="contacts"),
]
