from django.contrib import admin
from .models import Customer, BarberService, BarberShop, Barber, Appointment, Products, Order, OrderItem


admin.site.register(Customer)
admin.site.register(BarberService)
admin.site.register(BarberShop)
admin.site.register(Barber)
admin.site.register(Appointment)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(OrderItem)