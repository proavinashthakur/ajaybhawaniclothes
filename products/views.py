# from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . serializers import ProductSerializer
from . models import Products


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product endpoints.
    """
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [IsAuthenticated]