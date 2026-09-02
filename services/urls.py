from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subcategory/<int:sub_category_id>/', views.subcategory_detail, name='subcategory_detail'),
]