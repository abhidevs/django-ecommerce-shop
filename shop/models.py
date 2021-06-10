from django.db import models
from datetime import datetime


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500)
    price = models.IntegerField(default=0)
    list_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="shop/images", default="")


    def __str__(self):
        return f'{self.product_name} - {self.category} - {self.price} - {self.list_date}'
    

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    message = models.CharField(max_length=1000, default="")


    def __str__(self):
        return f'{self.name} - {self.email} - {self.message}'
    

class CartItem(models.Model):
    cartItem_id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.product_id} - {self.quantity}'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=50)
    address_id = models.CharField(max_length=50)
    product_id = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    pricePerItem = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_id} - {self.quantity} - {self.customer_id} - {self.order_date}'


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    phone = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.email} - {self.phone}'
    

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    customer_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    phone = models.IntegerField(default=0)
    optPhone = models.IntegerField(default=0)
    address = models.CharField(max_length=250, default="")
    state = models.CharField(max_length=25, default="")
    city = models.CharField(max_length=25, default="")
    zip = models.CharField(max_length=6, default="")
    landmark = models.CharField(max_length=25, default="")

    def __str__(self):
        return f'{self.name} - {self.state} - {self.city} - {self.zip}'
    