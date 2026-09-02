from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CustomerProfile, CustomerAddress, ProviderProfile

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('phone', 'is_customer', 'is_provider', 'is_staff')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Roles', {'fields': ('is_customer', 'is_provider')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_customer', 'is_provider'),
        }),
    )
    search_fields = ('phone',)
    ordering = ('phone',)

class CustomerAddressInline(admin.TabularInline):
    model = CustomerAddress
    extra = 1

class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_full_name', 'user_email', 'city')
    inlines = (CustomerAddressInline,)
    readonly_fields = ('user_full_name', 'user_email')

    def user_full_name(self, obj):
        return obj.user.first_name or '-'
    user_full_name.short_description = 'Full Name'

    def user_email(self, obj):
        return obj.user.email or '-'
    user_email.short_description = 'Email'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_customer=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'city')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_provider=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(User, UserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(CustomerAddress)

admin.site.register(ProviderProfile, ProviderProfileAdmin)