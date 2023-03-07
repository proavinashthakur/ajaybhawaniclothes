
# rest framework
from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny, IsAuthenticated


# django
from django.urls import reverse
from django.conf import settings


# Ajay Bhawani
from .serializers import (
    UserLoginSerializer,
    UserLogoutSerializer,
    UserRegistrationSerializer
)


class UserRegisterationView(generics.CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """New user registration endpoint."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return response.Response(user_data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """User login endpoint."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class UserLogoutView(generics.CreateAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """User logout endpoint."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(status=status.HTTP_204_NO_CONTENT)




