from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    full_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = PhoneNumberField(null=True)

    username = models.CharField(max_length=200, unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class BarberService(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class BarberShop(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='barbershop_photos/', null=True)

    def __str__(self):
        return self.name
    
class Barber(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='barber_photos/', null=True)

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    barbershop_name = models.CharField(max_length=200)
    barber_name = models.CharField(max_length=200)
    service_name = models.CharField(max_length=200)
    service_price = models.DecimalField(max_digits=6, decimal_places=2)
    selected_date = models.CharField()
    selected_time = models.CharField()

class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products_photos/', null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    data_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
