from django import forms

from BlogHaven.models import Blog


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ["title", "slug", "content", "image", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }
