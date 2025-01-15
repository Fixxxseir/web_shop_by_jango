from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from catalog.models import Product


class Command(BaseCommand):

	def handle(self, *args, **options):
		group, created = Group.objects.get_or_create(name='Модераторы продуктов')

		can_unpublish_product = Permission.objects.get(codename='can_unpublish_product')
		delete_product = Permission.objects.get(config='delete_product')

		group.permissions.add(can_unpublish_product, delete_product)

		if created:
			self.stdout.write(self.style.SUCCESS('Группа модераторов продуктов успешно создана'))

