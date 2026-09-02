from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import CustomerProfile, CustomerAddress
from services.models import Service
from .models import CartItem, Booking, BookingSession

@login_required
def add_to_cart(request, service_id):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    service = get_object_or_404(Service, id=service_id)

    cart_item, created = CartItem.objects.get_or_create(
        customer=profile,
        service=service,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{service.name} added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'subcategory_detail'))

@login_required
def customer_cart(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    cart_items = profile.cart_items.select_related('service')
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'bookings/customer_cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, item_id):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, customer=profile)
    cart_item.delete()
    # messages.success(request, f"{cart_item.service.name} removed from cart.")
    return redirect('customer_cart')

@login_required
def checkout(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    addresses = profile.addresses.all()

    if request.method == 'POST':
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        address = get_object_or_404(CustomerAddress, id=address_id, customer=profile)

        session = BookingSession.objects.create(
            customer=profile,
            status='Pending',
            payment_method=payment_method
        )

        # Convert cart items into bookings
        for item in profile.cart_items.all():
            Booking.objects.create(
                session=session,
                service=item.service,
                address=address,
                price=item.service.price
            )

        profile.cart_items.all().delete()

        messages.success(request, "Checkout successful! Your booking is confirmed.")
        return redirect('customer_bookings')

    return render(request, 'bookings/checkout.html', {'addresses': addresses})

@login_required
def customer_bookings(request):
    profile = get_object_or_404(CustomerProfile, user=request.user)
    sessions = BookingSession.objects.filter(customer=profile).order_by('-created_at')

    # add total per session
    for session in sessions:
        session.total = sum(b.price for b in session.bookings.all() if b.price is not None)

    # grand total across all session
    total_amount = sum(session.total for session in sessions)

    return render(request, 'bookings/customer_bookings.html', {'sessions': sessions, 'total_amount': total_amount})
