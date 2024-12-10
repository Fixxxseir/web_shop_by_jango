from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from catalog.models import Product, Contact, Category
from catalog.forms import ProductForm


def home(request):
    latest_products = Product.objects.order_by("-created_at")[:5]
    print(f"Крайние 5 созданных продуктов: {latest_products}")
    return render(request, "catalog/home.html")


def contacts(request):
    contacts_list = Contact.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Данные успешно отправлены.")
    return render(request, "catalog/contacts.html", {"contacts": contacts_list})


def catalog(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)

    page_number = request.GET.get("page")
    paginator_products = paginator.get_page(page_number)

    context = {"products": paginator_products, "paginator": paginator}
    return render(request, "catalog/catalog.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "catalog/product_detail.html", context)


def add_product(request):
    categories = Category.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("catalog:catalog")
    else:
        form = ProductForm()

    return render(request, "catalog/add_product.html", {"form": form, "categories": categories})
