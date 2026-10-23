from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from cart.models import Cart
from rest_framework import serializers
from cart.serializer import CartSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class CartView(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user = self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity',1)
        if quantity < 1:
            return Response(data={"msg":"Invalid quantity"})

        cart = Cart.objects.filter(user = self.request.user,product = product).first()
        if cart:
            total_quantity = cart.quantity + quantity
            if total_quantity > product.stock + cart.quantity:
                raise serializers.ValidationError({f"Not enough,{product.name} is out of stock"})
            cart.quantity = total_quantity
            cart.save()

        else:
            if quantity > product.stock:
                raise serializers.ValidationError({f"Not enough,{product.name} is out of stock"})
            
            serializer.save(user=self.request.user)
        product.stock -= quantity
        product.save()

    def destroy(self, request, *args, **kwargs):
        cart_id = self.get_object()
        if cart_id.user != request.user:
            return Response(data={"error":"The user is invalid"})
        cart_id.delete()
        return Response(data={"msg":"The cart is deleted"})
        