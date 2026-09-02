from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerAddress

class CustomerSignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        return user

class CustomerLoginForm(forms.Form):
    phone = forms.CharField(max_length=10, required=True)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomerProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre fill fields if name available
        if self.instance.first_name:
            self.fields['full_name'].initial = self.instance.first_name

    def save(self, commit=True):
        user = super().save(commit=False)
        # split full_name into first and last name
        user.first_name = self.cleaned_data.get('full_name', '')
        if commit:
            user.save()
        return user

class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ['house_no', 'area', 'pin_code', 'landmark', 'town_city', 'state']
        labels = {'house_no': 'House No', 'area': 'Area', 'pin_code': 'Pin Code', 'landmark': 'Landmark', 'town_city': 'Town/City', 'state': 'State'}