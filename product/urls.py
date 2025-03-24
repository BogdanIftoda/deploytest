from rest_framework.routers import DefaultRouter

from product.views import CategoryViewSet, ProductViewSet

app_name = "product"
router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')

urlpatterns = router.urls
