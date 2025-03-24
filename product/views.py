from django_filters.rest_framework import DjangoFilterBackend
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from product.filters import ProductFilter
from product.models import Category, Product
from product.permissions import RBACCategoryPermission
from product.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.get_category_tree()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, RBACCategoryPermission)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category", "seller").filter(is_approved=True)
    serializer_class = ProductSerializer
    # permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    authentication_classes = (OAuth2Authentication)
    filterset_class = ProductFilter
    search_fields = ("name", "^description")
    ordering_fields = ("price",)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
