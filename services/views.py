from django.shortcuts import render, get_object_or_404
from .models import Category, SubCategory
from users.models import CustomerProfile


def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def subcategory_detail(request, sub_category_id):
    subcategory = get_object_or_404(SubCategory, id=sub_category_id)
    services = subcategory.services_sub_category.all()

    cart_service_ids = []
    if request.user.is_authenticated:
        profile = get_object_or_404(CustomerProfile, user=request.user)
        cart_service_ids = list(profile.cart_items.values_list('service_id', flat=True))

    return render(request, 'services/subcategory_services.html',
                  {'subcategory': subcategory, 'services': services, 'cart_service_ids': cart_service_ids}
                  )