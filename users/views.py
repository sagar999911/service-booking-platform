from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerSignUpForm, CustomerLoginForm
from django.contrib.auth.decorators import login_required
from .forms import CustomerProfileForm, CustomerAddressForm
from .models import CustomerAddress, CustomerProfile

# def home(request):
#     form = CustomerSignUpForm()
#     return render(request, 'home.html', {'form': form})

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login')
            return redirect('home')
    else:
        form = CustomerSignUpForm()
    return render(request, 'users/customer_register.html', {'form': form})

def customer_login(request):
    if request.method =='POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            user = authenticate(request, phone=phone, password=password)
            if user is not None and user.is_customer:
                login(request, user)
                messages.success(request, 'Logged in sucessfully')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = CustomerLoginForm()
    return render(request, 'users/customer_login.html', {'form': form})

def customer_logout(request):
    logout(request)
    messages.info(request, 'You have Logged out')
    return redirect('home')

@login_required
def customer_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('customer_profile')
    else:
        form = CustomerProfileForm(instance=user)

    return render(request, 'users/customer_profile.html', {'form': form})

@login_required
def customer_address_list(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    address_list = profile.addresses.all()
    return render(request, 'users/customer_address.html', {'address_list': address_list})

@login_required
def customer_address_create(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    if request.method == 'POST':
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = profile
            address.save()
            messages.success(request, 'Address Added successfully')
            return redirect('customer_address_list')
    else:
        form = CustomerAddressForm()
    return render(request, 'users/customer_address_form.html', {'form': form})


@login_required
def customer_address_edit(request, pk):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    address = get_object_or_404(CustomerAddress, pk=pk, customer=profile)
    if request.method == 'POST':
        form = CustomerAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully')
            return redirect('customer_address_list')
    else:
        form = CustomerAddressForm(instance=address)
    return render(request, 'users/customer_address_form.html', {'form': form})

@login_required
def customer_address_delete(request, pk):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    address = get_object_or_404(CustomerAddress, pk=pk, customer=profile)
    address.delete()
    messages.success(request, 'Address deleted successfully')
    return redirect('customer_address_list')