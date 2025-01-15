from django.db import models
from django.urls import reverse

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Наименование категории", help_text="Введите наименование категории"
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание категории", help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ("not_published", "Не опубликовано"),
        ("published", "Опубликовано"),
    ]
    name = models.CharField(
        max_length=150, verbose_name="Наименование продукта", help_text="Введите наименование продукта"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        help_text="Введите категорию продукта",
        null=True,
        blank=True,
        related_name="products",
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание продукта", help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_to="products/images",
        blank=True,
        null=True,
        verbose_name="Изображение продукта",
        help_text="Загрузите изображение продукта",
    )
    purchase_price = models.FloatField(verbose_name="Цена продукта", help_text="Введите цену продукта")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата последнего изменения")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="not_published")
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца продукта",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = [
            "name",
            "category",
            "purchase_price",
        ]
        permissions = [
            ("can_unpublish_product", "can unpublish product"),
        ]

    def __str__(self):
        return f"'{self.name}' в категории: {self.category}"

    def get_absolute_url(self):
        return reverse("catalog:product_detail", kwargs={"product_slug": self.slug})


class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя для связи", help_text="Введите контактное имя")
    phone = models.CharField(max_length=16, verbose_name="Номер для связи", help_text="Введите контактный номер")
    email = models.EmailField(verbose_name="Почта для связи", help_text="Введите свою контактную почту")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name
