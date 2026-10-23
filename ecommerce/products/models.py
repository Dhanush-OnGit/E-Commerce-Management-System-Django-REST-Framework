from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    describtion = models.TextField(max_length=100,blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="product")
    name = models.CharField(max_length=100)
    describtion = models.TextField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=4)
    stock = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="product",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name