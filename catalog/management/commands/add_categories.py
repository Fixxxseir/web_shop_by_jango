from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category


class Command(BaseCommand):
	help = " Добавление продуктов в БД с помощью фикстуры "

	def handle(self, *args, **kwargs):
		Category.objects.all().delete()

		call_command('loaddata', 'catalog_category_fixture.json')
		self.stdout.write(self.style.SUCCESS('Успешное добавление данных в БД'))
