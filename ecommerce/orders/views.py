from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from orders.models import Order,OrderItem,OrderStatusHistory
from cart.models import Cart
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from orders.models import Payment
from rest_framework.decorators import action
from orders.serializer import OrderItemSerializer,OrderSerializer
from django.core.mail import send_mail

# Create your views here.

class OrderView(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.role == "admin":
            return Order.objects.all()
        return Order.objects.filter(user = self.request.user)

    def create(self, request, *args, **kwargs):
        cart_item = Cart.objects.filter(user=request.user)
        if not cart_item.exists():
            return Response(data={"msg":"The cart is empty"},status=status.HTTP_404_NOT_FOUND)

        payment_method = request.data.get("payment_method")
        if payment_method not in ["cod","online"]:
            return Response(data={"error":"Invalid payment method"},status=status.HTTP_400_BAD_REQUEST)

        total = 0
        for i in cart_item:
            total += i.product.price * i.quantity

        payment_status = "success"
        if payment_status != "success":
            return Response(data={"msg":"Payment if failed"})
        
        order = Order.objects.create(user=request.user,total_price=total,status="confirmed")

        for j in cart_item:
            OrderItem.objects.create(order=order,product=j.product,quantity=j.quantity,price=j.product.price)
            # product = j.product
            # product.stock -= j.quantity
            # product.save()

        payment = Payment.objects.create(order=order,payment_method=payment_method,amount=total,status="success")
        OrderStatusHistory.objects.create(order=order,status="confirmed")
        cart_item.delete()
        send_mail(
            subject="Order Conformation Email",
            message=f"""
        Hello {request.user.username},
        Your order is conformed successfully.
        Order id : {order.id}
        payment id : {payment.id}
        Total amount : {order.total_price}
        payment status : {payment.status}
        payment method : {payment.payment_method}
        Thankyou for your order    
        """,
            from_email="PROJECTgmail@gmail.com",
            recipient_list=[request.user.email],
            fail_silently=False
        )
        
        serializer = OrderSerializer(order)
        return Response(data={
            "msg":"Order confirmed",
            "order id" : order.id,
            "payment id" : payment.id,
            "payment status" : payment.status,
            'payment method' : payment.payment_method,
            "order" : serializer.data
        })
       
    @action(detail=True,methods=["post"])
    def cancel(self,request,*args,**kwargs):
        order = self.get_object()
        if order.user != request.user:
            return Response(data={"msg":"Invalid user"},status=status.HTTP_400_BAD_REQUEST)
        if order.status == "delivered":
            return Response(data={f"The order is already delivered"})
        elif order.status == "cancelled":
            return Response(data={"error":"The order is already cancelled"})

        product_name = []
        for i in order.items.all():
            product = i.product
            product.stock += i.quantity
            product.save()
            product_name.append(product.name)
        
        order.status = "cancelled"
        order.save()
        OrderStatusHistory.objects.create(order=order,status="cancelled")
        send_mail(
            subject="Order cancelled successfully",
            message=f"""
        Hey {request.user.username}
        Your order is cancelled succesfull
        order id : {order.id}
        product name : {product.name}
        order status : {order.status}
        """,
            from_email=None,
            recipient_list=[request.user.email],
            fail_silently=False
        )
        return Response(data={f"The {order.user.username}'s order is cancelled"})

    @action(detail=True,methods=["patch"])
    def update_status(self,request,*args,**kwargs):
        if self.request.user.role != "admin":
            return Response(data={"msg":"Only admin can perform this action"})
        order = self.get_object()
        new_status = request.data.get("status")
        if new_status not in ["pending","confirmed","shipped","delivered"]:
            return Response(data={"error":"Invalid status"})
        order.status = new_status
        order.save()
        OrderStatusHistory.objects.create(order=order,status=new_status)
        serilaizer = OrderSerializer(order)
        return Response(data= serilaizer.data)

    @action(detail=True,methods=["get"])
    def tracking(self,request,*args,**kwargs):
        order = self.get_object()
        status_history = []
        for i in order.status_history.all():
            status_history.append({"status":i.status,"created_at":i.created_at}) 
        return Response(data={
            "order id" : order.id,
            "current status": order.status,
            "status_history" : status_history
        },status=status.HTTP_201_CREATED)


    @action(detail=True,methods=["post"])
    def payment(self,request,*args,**kwargs):
        order = self.get_object()
        if order.user != request.user:
            return Response(data={"error":"invalid user"})
        if order.status == "delivered":
            return Response(data={"msg":"The order is already delivered"},status=status.HTTP_400_BAD_REQUEST)
        if order.status == "cancelled":
            return Response(data={"msg":"The order is already cancelled"},status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Payment.objects.get(order=order)
            return Response(data={"msg":"payment already exists","payment_status":product.status},status=status.HTTP_400_BAD_REQUEST)
        except Payment.DoesNotExist:
            payment_method = request.data.get("payment_method")
            if payment_method not in ["cod","online"]:
                return Response(data={"error":"Invalid payment method"},status=status.HTTP_400_BAD_REQUEST)
            payment = Payment.objects.create(order=order,amount=order.total_price,payment_method=payment_method,status="success")
            return Response(data={
                "msg":"payment created",
                "payment id": payment.id,
                "order id" : order.id,
                "amount" : order.total_price,
                "payment method" : payment_method,
                "status" : payment.status
            },status=status.HTTP_201_CREATED)
        
        