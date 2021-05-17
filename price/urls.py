from django.urls import path
from .views import prices_list, price_detail

urlpatterns = [
    path('<slug:slug>/', price_detail, name='price_detail'),
    path('', prices_list, name='prices_list'),
]