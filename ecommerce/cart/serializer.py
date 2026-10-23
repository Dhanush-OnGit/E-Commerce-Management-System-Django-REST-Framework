from rest_framework import serializers
from cart.models import Cart

class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product_name = serializers.CharField(source="product.name",read_only=True)
    product_price = serializers.DecimalField(source = "product.price",read_only=True,max_digits=10,decimal_places=3)
    class Meta:
        model = Cart
        fields = ["id","user","product","quantity","added_at","product_name","product_price"]
        read_only_fields = ["id","added_at","user"]