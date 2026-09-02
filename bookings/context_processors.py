from .models import CartItem
from users.models import CustomerProfile

def cart_count(request):
    if request.user.is_authenticated:
        try:
            profile =CustomerProfile.objects.get(user=request.user)
            count = CartItem.objects.filter(customer=profile).count()
            return {'cart_count': count}
        except CustomerProfile.DoesNotExist:
            return {'cart_count': 0}
    return {'cart_count': 0}