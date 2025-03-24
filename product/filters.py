import django_filters

from product.models import Product


class ProductFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()
    seller = django_filters.CharFilter(field_name='seller__username', lookup_expr='icontains')
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')

    class Meta:
        model = Product
        fields = ['price', 'category', 'seller']

    @staticmethod
    def filter_in_stock(queryset, name, value):
        return queryset.filter(stock__gt=0) if value else queryset.filter(stock=0)
