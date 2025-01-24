from django.urls import path

from BlogHaven.apps import BloghavenConfig
from BlogHaven.views import BlogCreateView, BlogDeleteView, BlogDetailView, BlogListView, BlogUpdateView

app_name = BloghavenConfig.name


urlpatterns = [
    path("blog/", BlogListView.as_view(), name="blog_list"),
    path("blog/new/", BlogCreateView.as_view(), name="blog_create"),
    path("blog/post/<slug:blog_slug>/", BlogDetailView.as_view(), name="blog_detail"),
    path("blog/update/<slug:slug>/", BlogUpdateView.as_view(), name="blog_update"),
    path("blog/delete/<slug:slug>/", BlogDeleteView.as_view(), name="blog_delete"),
]
