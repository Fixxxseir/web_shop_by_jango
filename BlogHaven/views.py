from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from BlogHaven.models import Blog
from BlogHaven.forms import BlogForm


class BlogListView(ListView):
	model = Blog

	def get_queryset(self):
		return super().get_queryset().filter(is_published=Blog.Status.PUBLISHED)


class BlogCreateView(CreateView):
	model = Blog
	form_class = BlogForm
	success_url = reverse_lazy("BlogHaven:blog_list")


class BlogDetailView(DetailView):
	model = Blog
	slug_field = 'slug'
	slug_url_kwarg = 'blog_slug'

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		obj.view_counter += 1
		obj.save()
		if obj.view_counter >= 24 and not obj.is_notification_sent:
			self.send_notification(obj)
		return obj

	def send_notification(self, blog):
		subject = 'Уведомление о просмотрах'
		message = f'Ваша статья {blog.title} набрала 20 просмотров!'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ['example@gmail.com']

		# Отправьте письмо
		send_mail(subject, message, email_from, recipient_list)

		# Обновите флаг is_notification_sent, чтобы письмо отправлялось только один раз
		blog.is_notification_sent = True
		blog.save()


class BlogUpdateView(UpdateView):
	model = Blog
	form_class = BlogForm

	def get_object(self, queryset=None):
		slug = self.kwargs.get('slug')
		return get_object_or_404(Blog, slug=slug)

	def get_success_url(self):
		# blog = self.get_object()
		return reverse('BlogHaven:blog_detail', args=[self.kwargs.get('slug')])
		# args=[self.kwargs.get('blog_slug')])


class BlogDeleteView(DeleteView):
	model = Blog
	success_url = reverse_lazy("BlogHaven:blog_list")

	def get_object(self, queryset=None):
		slug = self.kwargs.get('slug')
		return get_object_or_404(Blog, slug=slug)

