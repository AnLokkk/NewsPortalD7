from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import *


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='Category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Выберите категорию',
    )

    date = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='по дате',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
        }