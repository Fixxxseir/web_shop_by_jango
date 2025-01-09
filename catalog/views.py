from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

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


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = "product_slug"

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs[self.slug_url_kwarg])


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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    slug_url_kwarg = "update_slug"

    def get_success_url(self):
        return reverse("catalog:product_detail", args=[self.kwargs.get("update_slug")])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories": Category.objects.all(),
                "main_title": "Здесь вы можете изменить свой товар",
                "sub_title": "Всегда ждём вашу обратную связь:)",
                "main_link": "catalog:home",
                "main_link_text": "На главную",
                "sub_link": "catalog:product_list",
                "sub_link_text": "Назад к покупкам",
            }
        )
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")
