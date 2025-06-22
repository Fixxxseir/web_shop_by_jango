from django import template

register = template.Library()


@register.filter(name="media_filter_blog")
def media_filter_blog(path):
    if path:
        return f"/media/{path}"
    return "#"
