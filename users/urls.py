from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserRegisterView, email_verification, UserEditProfile

app_name = UsersConfig.name

urlpatterns = [
	path('login/', LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', LogoutView.as_view(next_page='catalog:home'), name='logout'),
	path('register/', UserRegisterView.as_view(), name='register'),
	path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
	path('edit/', UserEditProfile.as_view(), name='edit_profile')
	]
