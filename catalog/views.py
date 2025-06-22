from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden, request
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Category, Contact, Product
from catalog.services import ProductServices


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

    def get_queryset(self):
        return ProductServices.get_products_from_cache()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     paginator = Paginator(self.get_queryset(), self.paginate_by)
    #     page = self.request.GET.get("page", 1)
    #     products = paginator.page(page)
    #     context["products"] = products
    #
    #     return context


class CategoryProductListView(ListView):
    model = Product
    template_name = "catalog/category_product.html"
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.kwargs["category_id"]

        context["object_list"] = ProductServices.get_product_by_category(category_id)
        context["categories"] = Category.objects.all()

        return context


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = "product_slug"

    def get_object(self, queryset=None):
        return get_object_or_404(Product, slug=self.kwargs[self.slug_url_kwarg])


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)

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

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product") and user.has_perm("catalog.delete_product"):
            return ProductModeratorForm
        raise PermissionDenied("Нет прав на изменение или удаление продукта")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")
    permission_required = "catalog.delete_product"

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        user = self.request.user

        if product.owner == user or user.has_perm("catalog.delete_product"):
            return product

        raise PermissionDenied("Нет прав на удаление продукта")


class StatusProductView(LoginRequiredMixin, View):
    slug_url_kwarg = "product_slug"

    def post(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)

        if not request.user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden("У вас нет прав для изменения статуса продукта")

        if product.status == "not_published":
            product.status = "published"
        else:
            product.status = "not_published"
        product.save()

        return redirect("catalog:product_detail", product_slug=product_slug)
