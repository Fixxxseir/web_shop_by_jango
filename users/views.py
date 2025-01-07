import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.core.mail import send_mail
from .forms import UserRegisterForm, UserEditForm

from config.settings import EMAIL_HOST_USER
from .models import User


class UserRegisterView(CreateView):
	model = User
	form_class = UserRegisterForm
	template_name = 'users/register.html'
	success_url = reverse_lazy('users:login')

	def form_valid(self, form):
		user = form.save()  #получение пользователя
		user.is_active = False
		token = secrets.token_hex(16)
		user.token = token
		user.save()
		host = self.request.get_host()
		url = f'http://{host}/users/email-confirm/{token}/'
		send_mail(
			subject="Подтверждение почты",
			message=f"Переход по ссылке для подтверждения почты {url}",
			from_email=EMAIL_HOST_USER,
			recipient_list=[user.email]
		)

		return super().form_valid(form)


def email_verification(request, token):
	user = get_object_or_404(User, token=token)
	user.is_active = True
	user.save()
	return redirect(reverse("users:login"))


class UserEditProfile(LoginRequiredMixin, UpdateView):
	model = User
	form_class = UserEditForm
	template_name = 'users/user_edit_form.html'
	success_url = reverse_lazy('catalog:home')

	def get_object(self, queryset=None):
		return self.request.user