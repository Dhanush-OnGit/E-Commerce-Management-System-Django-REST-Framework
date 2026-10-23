from django.shortcuts import render
from rest_framework.permissions import BasePermission
from products.serializer import CategorySerializer,ProductSerilaizer
from products.models import Category,Product
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
# Create your views here.

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_authenticated and request.user.role == "admin"

class CategoryView(ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class ProductView(ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = ProductSerilaizer
    queryset = Product.objects.all()
    filter_backends = [SearchFilter]
    Search_fields = ["category"]