from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Product


def home(request):
	latest_products = Product.objects.order_by('-created_at')[:5]
	print(f'Последние 5 создпоследнийанных продуктов: {latest_products}')
	return render(request, 'catalog/home.html')


def contacts(request):
	if request.method == "POST":
		name = request.POST.get("name")
		phone = request.POST.get("phone")
		message = request.POST.get("message")
		return HttpResponse(f"Спасибо, {name}! Данные успешно отправлены.")
	return render(request, 'catalog/contacts.html')
