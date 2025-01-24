from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm
from django.utils.deconstruct import deconstructible

from catalog.models import Category, Product


@deconstructible
class ForbiddenWordsValidator:
    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "дёшево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]
    code = "stop_word"

    def __init__(self, message=None):
        self.message = message if message else "Запретное слово, такое нельзя"

    def __call__(self, value, *args, **kwargs):
        for word in self.FORBIDDEN_WORDS:
            if word in value.lower():
                raise ValidationError(self.message, code=self.code)


class StyleProductMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleProductMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ["name", "slug", "category", "description", "image", "purchase_price"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Введите наименование продукта"})
        self.fields["name"].validators.append(ForbiddenWordsValidator())
        self.fields["slug"].widget.attrs.update({"placeholder": "Введите slug"})
        self.fields["category"].widget.attrs.update({"class": "form-control", "label": "категория не выбрана"})
        self.fields["category"].empty_label = "Категория не выбрана"
        self.fields["description"].widget.attrs.update({"placeholder": "Введите описание продукта"})
        self.fields["description"].validators.append(ForbiddenWordsValidator())
        self.fields["image"].widget.attrs.update({"class": "form-control-file"})
        self.fields["purchase_price"].widget.attrs.update({"placeholder": "Введите цену продукта"})

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data["purchase_price"]
        if purchase_price <= 0:
            raise ValidationError("Цена продукта не может быть отрицательной")
        return purchase_price

    def clean_image(self):
        image = self.cleaned_data["image"]
        if image:
            if not image.name.lower().endswith((".jpeg", ".png", ".jpg")):
                raise ValidationError("Фото неверного формата")

            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Фото не должно превышать 5 МБ")

        return image


class ProductModeratorForm(StyleProductMixin, ModelForm):
    class Meta:
        model = Product
        fields = ("status",)
