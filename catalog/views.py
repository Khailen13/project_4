from django.http import HttpResponse
from django.shortcuts import render

from .models import Product


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        return HttpResponse(f"Спасибо, {name}! Сообщение получено.")
    return render(request, "product/contacts.html")


def main(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "product/index.html", context)


def product(request, pk):
    product = Product.objects.get(id=pk)
    context = {"product": product}
    return render(request, "product/product.html", context)
