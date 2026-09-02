from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# Custom Manager
class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number required')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    username = None
    phone = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_customer = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

# Customer Section
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"Customer :- {self.user.phone}"

class CustomerAddress(models.Model):
    customer = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE, related_name='addresses')
    house_no = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    town_city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.customer.user.phone} -> {self.house_no}, {self.town_city}"

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    def __str__(self):
        return f"Provider {self.business_name}"