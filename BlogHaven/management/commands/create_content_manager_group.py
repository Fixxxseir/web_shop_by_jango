from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from BlogHaven.models import Blog


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        group, created = Group.objects.get_or_create(name="Контент-менеджеры")

        content_type = ContentType.objects.get_for_model(Blog)
        permissions = [
            "add_blog",
            "change_blog",
            "delete_blog",
            "can_publish_post",
        ]

        for perm in permissions:
            permission = Permission.objects.filter(codename=perm, content_type=content_type).first()
            if permission:
                group.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f"Добавлено разрешение {perm} к группе Контент-менеджер"))
            else:
                self.stdout.write(self.style.WARNING(f"Разрешение {perm} не найдено"))
