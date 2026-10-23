from django.db import models
from accounts.models import User
from products.models import Product
# Create your models here.

class Order(models.Model):
    STATUS_OPTION = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="order")
    total_price = models.DecimalField(decimal_places=2,max_digits=10,default=0)
    status = models.CharField(choices=STATUS_OPTION,max_length=50,default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.product} x {self.quantity}"

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="status_history")
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.id} - {self.status}"


class Payment(models.Model):
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed")
    ]
    PAYMENT_METHOD = [
        ("cod", "Cash on Delivery"),
        ("online", "Online Payment")
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    order = models.OneToOneField(Order,on_delete=models.CASCADE,related_name="payment")
    amount = models.DecimalField(decimal_places=10,max_digits=10)
    payment_method = models.CharField(max_length=100,choices=PAYMENT_METHOD)
    status = models.CharField(max_length=100,choices=PAYMENT_STATUS,default="success")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order -{self.order.id}"