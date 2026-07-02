from django.contrib import admin
from shop.models import Cart, Categories, Checkout, OrderItem, Product, Profile

# Register your models here.

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Checkout)
admin.site.register(Profile)
admin.site.register(OrderItem)