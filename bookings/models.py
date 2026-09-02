from django.db import models
from users.models import CustomerProfile, CustomerAddress
from services.models import Service

class CartItem(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='cart_items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.service.price

    def __str__(self):
        return f"{self.service.name} ({self.quantity})"

class BookingSession(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='booking_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[('Cash', 'Cash'), ('Online', 'Online')], default='Cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

class Booking(models.Model):
    session = models.ForeignKey(BookingSession, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.ForeignKey(CustomerAddress, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # def __str__(self):
    #     return f"{self.customer.user.username} - {self.service.name}"