import django_filters
from .models import *


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    author = django_filters.CharFilter(field_name="author__user__username", lookup_expr="icontains")
    class Meta:
        models = Book
        fields = ("author__user__username", "title",)