import django_filters
from django.db.models import Q
from .models import Sale

class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass

class SaleFilter(django_filters.FilterSet):
    customer_region = CharInFilter(field_name='customer__region', lookup_expr='in')
    gender = CharInFilter(field_name='customer__gender', lookup_expr='in')
    product_category = CharInFilter(field_name='product__category', lookup_expr='in')
    payment_method = CharInFilter(field_name='payment_method', lookup_expr='in')
    tags = CharInFilter(method='filter_tags')
    age_min = django_filters.NumberFilter(field_name='customer__age', lookup_expr='gte')
    age_max = django_filters.NumberFilter(field_name='customer__age', lookup_expr='lte')
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Sale
        fields = []

    def filter_tags(self, queryset, name, value):
        # value is comma-separated list
        tag_names = []
        if isinstance(value, (list, tuple)):
            tag_names = value
        else:
            tag_names = [v.strip() for v in value.split(',') if v.strip()]
        if not tag_names:
            return queryset
        for tag in tag_names:
            queryset = queryset.filter(product__tags__name__iexact=tag)
        return queryset

