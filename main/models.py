
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email= models.EmailField(max_length=200, null=True)
    profile_pic = models.ImageField(default = "3.png" , null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor Item', 'Indoor Item'),
        ('Outdoor Item', 'Outdoor Item'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField( null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.TextField( null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('out of delivery', 'Out Of Delivery'),
        ('delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1200, null=True)

    def __str__(self):
        return self.product.name



 