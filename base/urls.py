from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.productsPage, name='products'),
    path('book/', views.bookPage, name='book'),
    path('products/<int:pk>/', views.productDetail, name='product_detail'),
    path('products/cart/', views.cartPage, name='cart_page'),
    path('products/checkout/', views.checkoutPage, name='checkout_page'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('products/<int:customer_id>/orders_page/', views.ordersPage, name='orders_page'),

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutCustomer, name='logout'),
    path('customer-account/<str:pk>/', views.updatePage, name='customer-account'),
    path('update-password/<str:pk>/', views.updatePassword, name='change-password'),
    
    path('book/barbershop/<str:barbershop_name>/', views.barbershop, name='barbershop'),
    path('book/services/<str:selected_barber>/', views.services, name='services'),
    path('book/choose_day/<int:service_id>/', views.chooseDay, name='choose_day'),
    path('book/choose_time/', views.chooseTime, name='choose_time'),
    path('book/appointment_confirmation/', views.appointmentConfirmation, name='appointment_confirmation'),
    path('book/save_appointment/', views.saveAppointment, name='save_appointment'),
    path('book/<str:full_name>/appointments_page/', views.appointmentsPage, name='appointments_page'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)