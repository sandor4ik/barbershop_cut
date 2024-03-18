from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import json
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .models import Customer, BarberService, BarberShop, Barber, Appointment, Products, Order, OrderItem
from .forms import MyCustomerCreationForm, CustomerForm, PasswordChangingForm


# Create your views here.
def home(request):
    barbers = Barber.objects.all()

    return render(request, 'base/home.html', {'barbers': barbers})

def productsPage(request):
    products = Products.objects.all()

    return render(request, 'base/products.html', {'products': products})

def productDetail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    
    return render(request, 'base/product_detail.html', {'product': product})

def cartPage(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'ger_cart_total':0, 'get_cart_items':0}

    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'base/cart_page.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user
    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def checkoutPage(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'ger_cart_total':0, 'get_cart_items':0}

    context = {
        'items': items,
        'order': order,
    }

    return render(request, 'base/checkout_page.html', context)

def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

    else:
        print('User is not logged in..')

    return JsonResponse('Order complete!', safe=False)

def ordersPage(request, customer_id):
    orders = Order.objects.filter(customer_id=customer_id)

    context ={
        'orders': orders,
    }
    return render(request, 'base/orders_page.html', context)

def bookPage(request):
    barbershops = BarberShop.objects.all()
    return render(request, 'base/book.html', {'barbershops': barbershops})

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            customer = Customer.objects.get(email=email)
        except:
            messages.error(request, 'Custromer doesn`t exist')

        customer = authenticate(request, email=email, password=password)

        if customer is not None:
            login(request, customer)
            return redirect('home')
        else:
            messages.error(request, 'Customer OR Password doesn`t exist')

    
    return render(request, 'base/register_login.html', {'page': page})

def logoutCustomer(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyCustomerCreationForm

    if request.method == 'POST':
        form = MyCustomerCreationForm(request.POST)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.email = customer.email.lower()
            customer.save()
            login(request, customer)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/register_login.html', {'form': form})

@login_required(login_url='login')
def updatePage(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer-account', pk=customer.id)

    context = {'customer': customer, 'form': form}
    return render(request, 'base/customer_account.html', context)

@login_required(login_url='login')
def updatePassword(request, pk):
    customer = Customer.objects.get(id=pk)
    form = PasswordChangingForm(user=request.user)
    
    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer-account', pk=customer.id)
    
    context = {'customer': customer, 'form': form}
    return render(request, 'base/change_password.html', context)

@login_required(login_url='login')
def barbershop(request, barbershop_name):

    if barbershop_name:
        if barbershop_name == 'CUTLER 1':
            barbers = Barber.objects.all()[:3]
            request.session['selected_barbershop'] = 'CUTLER 1'
            return render(request, 'base/barbershop1.html', {'barbers': barbers})
        
        elif barbershop_name == 'CUTLER 2':
            barbers = Barber.objects.all()[3:]
            request.session['selected_barbershop'] = 'CUTLER 2'
            return render(request, 'base/barbershop2.html', {'barbers': barbers})


@login_required(login_url='login')
def services(request, selected_barber=None):
    services = BarberService.objects.all()

    if selected_barber:
        request.session['selected_barber'] = selected_barber

    return render(request, 'base/services.html', {'services': services})

@login_required(login_url='login')
def chooseDay(request, service_id):
    selected_service = get_object_or_404(BarberService, id=service_id)

    request.session['selected_service'] = {
        'id' : selected_service.id,
        'name': selected_service.name,
        'price': float(selected_service.price),
        'duration': selected_service.duration,
    }
    return render(request, 'base/choose_day.html', {'selected_service': selected_service})

@login_required(login_url='login')
def chooseTime(request):
    selected_date = request.GET.get('selectedDate')
    request.session['selected_date'] = selected_date

    context = {
        'selected_date': selected_date,
    }

    return render(request, 'base/choose_time.html', context)

@login_required(login_url='login')
def appointmentConfirmation(request):

    selected_time = request.GET.get('selectedTime')
    request.session['selected_time'] = selected_time

    return render(request, 'base/appointment_confirmation.html', {})

@login_required(login_url='login')
def saveAppointment(request):
    selected_barbershop = request.session.get('selected_barbershop')
    selected_barber = request.session.get('selected_barber')
    selected_service_data = request.session.get('selected_service')
    selected_service_name = selected_service_data.get('name')
    selected_service_price = selected_service_data.get('price')
    selected_date = request.session.get('selected_date')
    selected_time = request.session.get('selected_time')

    if request.method == 'POST':
        customer = request.user
        full_name = customer.full_name
        email = customer.email
        phone_number = customer.phone_number

        appointment = Appointment(
            full_name = full_name,
            email = email,
            phone_number = phone_number,
            barbershop_name = selected_barbershop,
            barber_name = selected_barber,
            service_name = selected_service_name,
            service_price = selected_service_price,
            selected_date = selected_date,
            selected_time = selected_time,
        )
        
        appointment.save()

        del request.session["selected_barbershop"]
        del request.session["selected_barber"]
        del request.session["selected_service"]
        del request.session["selected_date"]
        del request.session["selected_time"]

        return render(request, 'base/save_appointment.html')
    
def appointmentsPage(request, full_name):
    appointments = Appointment.objects.filter(full_name=full_name)

    return render(request, 'base/appointments_page.html', {'appointments':appointments})