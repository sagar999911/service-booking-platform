from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('signup/customer/', views.customer_signup, name='customer_signup'),
    path('login/customer/', views.customer_login, name='customer_login'),
    path('logout/customer/', views.customer_logout, name='customer_logout'),
    path('profile/customer/', views.customer_profile, name='customer_profile'),

    path('addresses/', views.customer_address_list, name='customer_address_list'),
    path('addresses/add', views.customer_address_create, name='customer_address_create'),
    path('addresses/<int:pk>/edit/', views.customer_address_edit, name='customer_address_edit'),
    path('addresses/<int:pk>/delete/', views.customer_address_delete, name='customer_address_delete'),
]