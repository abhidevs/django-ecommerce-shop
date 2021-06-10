from django.contrib import admin

# Register your models here.
from .models import Product, Contact, CartItem, Orders, Customer, Address

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(CartItem)
admin.site.register(Orders)
admin.site.register(Customer)
admin.site.register(Address)
