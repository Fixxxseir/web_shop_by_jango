from django import forms
from catalog.models import Product, Category


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана",
                                      label='Категория продукта', widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = Product
        fields = ["name", "category", "description", "image", "purchase_price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "purchase_price": forms.NumberInput(attrs={"class": "form-control"}),
        }
