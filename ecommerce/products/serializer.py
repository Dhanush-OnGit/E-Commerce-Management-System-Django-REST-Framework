from rest_framework import serializers
from products.models import Category,Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id"]


class ProductSerilaizer(serializers.ModelSerializer):
    category_name = serializers.CharField(source ="category.name",read_only = True)
    class Meta:
        model = Product
        fields = ["id","category","name","describtion","price","stock","image","created_at","category_name"]
        read_only_fields = ["id","created_at"]