from django.forms import DateInput
from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post

class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    author = CharFilter(field_name='author__user__username',
                        lookup_expr='icontains')
    created_at = DateFilter(widget=DateInput(attrs={'type': 'date'}),
                   field_name='created_at', lookup_expr='gt')

    class Meta:
        model = Post
        fields = {'title', 'author', 'created_at'}