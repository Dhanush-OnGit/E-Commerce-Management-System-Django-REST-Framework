from rest_framework import serializers
from orders.models import Order,OrderItem,OrderStatusHistory,Payment

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name",read_only=True)
    class Meta:
        model = OrderItem
        fields = ["id","order","product","quantity","price","product_name"]
        read_only_fields = ["id","price"]

class OrderStatusHistorySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ["order","status","created_at"]
        read_only_fields = ["order","status","created_at"]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    items = OrderItemSerializer(many=True,read_only=True)
    status_history = OrderStatusHistorySerilaizer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ["id","user","total_price","status","created_at","items","status_history"]
        read_only_fields = ["id","user","total_price","status","created_at","items","status_history"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id","order","created_at","payment_method","amount","status"]
        read_only_fields = ["id","created_at","amount","status"]