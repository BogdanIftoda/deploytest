from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication.views import RegistrationView, ActivateView, UserViewSet

app_name = "authentication"
router = DefaultRouter()
router.register('users', UserViewSet, basename="users")

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("activate/<str:token>/", ActivateView.as_view(), name="activate"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
