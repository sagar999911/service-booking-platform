from django.contrib import admin
from .models import Booking, BookingSession

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    readonly_fields = ('service', 'price')

@admin.register(BookingSession)
class BookingSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'payment_method', 'status', 'created_at')
    inlines = [BookingInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'price')

    # def get_customer(self, obj):
    #     return obj.session.customer
    # get_customer.short_description = 'Customer'