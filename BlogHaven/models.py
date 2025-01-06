from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(is_published=Blog.Status.PUBLISHED)


class Blog(models.Model):
	class Status(models.IntegerChoices):
		DRAFT = 0, "Не опубликовано"
		PUBLISHED = 1, "Опубликовано"

	title = models.CharField(max_length=255, verbose_name="Заголовок", help_text="Введите название статьи")
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug")
	content = models.TextField(blank=True, verbose_name="Текст блога")
	image = models.ImageField(
		upload_to="BlogHaven/preview",
		blank=True,
		null=True,
		verbose_name="Превью",
		help_text="Загрузите изображение для превью"
	)
	created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
	is_published = models.BooleanField(choices=Status.choices, default=Status.PUBLISHED, verbose_name="Статус Публикации")
	view_counter = models.PositiveIntegerField(
		verbose_name="Счетчик просмотров",
		help_text="Укажите количество просмотров",
		default=0)

	class Meta:
		verbose_name = "Статья"
		verbose_name_plural = "Статьи"
		ordering = [
			"view_counter",
		]

	is_notification_sent = models.BooleanField(default=False)

	object = models.Manager
	published = PublishedManager()

	def get_absolute_url(self):
		return reverse("BlogHaven:blog_detail", kwargs={"blog_slug": self.slug})

	def __str__(self):
		return self.title
