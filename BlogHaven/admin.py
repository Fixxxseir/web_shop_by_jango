from django.contrib import admin
from BlogHaven.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "created_at", "is_published")
    list_filter = ("title",)
    search_fields = ("title", "created_at", "is_published")
