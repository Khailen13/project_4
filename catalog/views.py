from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ProductForm
from .models import Category, Product
from .services import get_category_products, get_products_from_cache


class ProductsListView(ListView):
    model = Product

    def get_queryset(self):
        return get_products_from_cache()


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        product = get_object_or_404(Product, id=product_id)
        if product.owner != request.user:
            return HttpResponseForbidden("Право редактирования есть только у владельца.")
        return super().post(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        product = get_object_or_404(Product, id=product_id)
        if not (request.user.has_perm("catalog.delete_product") or product.owner == request.user):
            return HttpResponseForbidden("У вас нет прав для удаления продукта.")
        product.delete()
        return redirect("catalog:product_list")


class ProductUnpublishView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        product = get_object_or_404(Product, id=product_id)

        if not request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied
        product.is_published = False
        product.save()
        return redirect("catalog:product_list")


class CategoryProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "catalog/category_product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        category_name = Category.objects.get(id=category_id)
        context["category_name"] = category_name
        context["products_in_category"] = get_category_products(category_id)
        return context


class ContactViews(LoginRequiredMixin, TemplateView):
    template_name = "catalog/contacts.html"
