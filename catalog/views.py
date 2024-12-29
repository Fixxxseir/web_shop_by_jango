from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from catalog.models import Product, Contact, Category
from catalog.forms import ProductForm


class ProductHomeView(View):
    template_name = "catalog/home.html"

    def get(self, request):
        latest_products = Product.objects.order_by("-created_at")[:5]
        print(f"Крайние 5 созданных продуктов: {latest_products}")

        context = {
            "main_title": "Добро пожаловать на наш сайт",
            "sub_title": "U can buy everything......",
            # 'main_link': 'catalog:home',
            "main_link_text": "Made by fixxseir",
            "sub_link": "catalog:contacts",
            "sub_link_text": "Дополнительная информация",
        }

        return render(request, self.template_name, context)


# def home(request):
#     latest_products = Product.objects.order_by("-created_at")[:5]
#     print(f"Крайние 5 созданных продуктов: {latest_products}")
#     context = {
#         'main_title': 'Добро пожаловать на наш сайт',
#         'sub_title': 'U can buy everything......',
#         # 'main_link': 'catalog:home',
#         'main_link_text': 'Made by fixxseir',
#         'sub_link': 'catalog:contacts',
#         'sub_link_text': 'Дополнительная информация',
#     }
#     return render(request, "catalog/home.html", context=context)


class ProductContactsView(View):
    template_name = "catalog/contacts.html"

    def get(self, request):
        contacts_list = Contact.objects.all()
        context = {
            "contacts": contacts_list,
            "main_title": "Спасибо, что посетили наш сайт",
            "sub_title": "Всегда ждём вашу обратную связь:)",
            "main_link": "catalog:home",
            "main_link_text": "На главную",
            "sub_link": "catalog:product_list",
            "sub_link_text": "Назад к покупкам",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Данные успешно отправлены.")


# def contacts(request):
#     contacts_list = Contact.objects.all()
#     if request.method == "POST":
#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         message = request.POST.get("message")
#         return HttpResponse(f"Спасибо, {name}! Данные успешно отправлены.")
#     context = {
#         "contacts": contacts_list,
#         'main_title': 'Спасибо, что посетили наш сайт',
#         'sub_title': 'Всегда ждём вашу обратную связь:)',
#         'main_link': 'catalog:home',
#         'main_link_text': 'На главную',
#         'sub_link': 'catalog:catalog',
#         'sub_link_text': 'Назад к покупкам',
#     }
#     return render(request, "catalog/contacts.html", context)


class ProductListView(ListView):
    model = Product
    paginate_by = 6

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     paginator = Paginator(self.get_queryset(), self.paginate_by)
    #     page = self.request.GET.get("page", 1)
    #     products = paginator.page(page)
    #     context["products"] = products
    #
    #     return context


# def catalog(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 6)
#
#     page_number = request.GET.get("page")
#     paginator_products = paginator.get_page(page_number)
#
#     context = {"products": paginator_products, "paginator": paginator}
#     return render(request, "catalog/catalog.html", context)


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs[self.slug_url_kwarg])

# def product_detail(request, product_slug):
#     product = get_object_or_404(Product, slug=product_slug)
#     context = {"product": product}
#     return render(request, "catalog/product_detail.html", context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories": Category.objects.all(),
                "main_title": "Здесь вы можете добавить свой товар",
                "sub_title": "Всегда ждём вашу обратную связь:)",
                "main_link": "catalog:home",
                "main_link_text": "На главную",
                "sub_link": "catalog:product_list",
                "sub_link_text": "Назад к покупкам",
            }
        )
        return context


# def add_product(request):
#     categories = Category.objects.all()
#
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             form.save()
#             return redirect("catalog:catalog")
#     else:
#         form = ProductForm()
#
#     context = {
#         "form": form,
#         "categories": categories,
#         'main_title': 'Здесь вы можете добавить свой товар',
#         'sub_title': 'Всегда ждём вашу обратную связь:)',
#         'main_link': 'catalog:home',
#         'main_link_text': 'На главную',
#         'sub_link': 'catalog:catalog',
#         'sub_link_text': 'Назад к покупкам',
#     }
#
#     return render(request, "catalog/add_product.html", context)
