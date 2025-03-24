from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from authentication.models import User, ActivationToken
from authentication.permissions import RBACUserPermission
from authentication.serializers import RegistrationSerializer, UserSerializer
from authentication.tasks import send_activation_email


class RegistrationView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            token = ActivationToken.objects.create(user=user)
            send_activation_email.delay(user.username, user.email, token.token)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    def get(self, request, token, **kwargs):
        try:
            token = ActivationToken.objects.get(token=token)
            if token.is_expired():
                return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
            user = token.user
            user.is_active = True
            user.save()
            token.delete()
        except ActivationToken.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)


@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(responses={status.HTTP_200_OK: UserSerializer}))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(request_body=UserSerializer,
                                                responses={status.HTTP_200_OK: UserSerializer}))
@method_decorator(name='partial_update',
                  decorator=swagger_auto_schema(request_body=UserSerializer,
                                                responses={status.HTTP_200_OK: UserSerializer}))
class UserViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, RBACUserPermission)
