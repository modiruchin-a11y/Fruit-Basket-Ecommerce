from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    
    def __str__(self):
        return self.user.username
    
    
    
class Categories(models.Model):
    cat_name=models.CharField(max_length=120)
    
    def __str__(self):
        return self.cat_name
    
class Product(models.Model):
    cat=models.ForeignKey(Categories, on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.IntegerField(default=1)
    description=models.TextField(max_length=130)
    image=models.ImageField(upload_to='images')
    is_published=models.BooleanField(default=False)
    
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_item=models.ForeignKey(Product,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.IntegerField(default=1)
    image=models.ImageField(upload_to='images')
    total_price=models.DecimalField(max_digits=10, decimal_places=2)

    
class Checkout(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('DELIVERED', 'Delivered'),
    ]
    PAYMENT_CHOICES = [
        ('RAZORPAY', 'Razorpay'),
        ('COD', 'Cash on Delivery'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    numbers = models.CharField(max_length=15)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20,choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING')
    razorpay_order_id = models.CharField(max_length=150, blank=True,null=True)
    


class OrderItem(models.Model):
    order = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)