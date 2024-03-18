from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Customer


class MyCustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'phone_number', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'email', 'phone_number']

class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = Customer
        fields = ['old_password', 'new_password1', 'new_password2']