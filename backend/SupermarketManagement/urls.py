from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customer', views.customer, name='customer'),
    path('inventory', views.inventory, name='inventory'),
    path('order', views.order, name='place_order'),
    path('purchase', views.purchase_return, name='purchase_return'),
    path('sales', views.sales_return, name='sales_return'),
    path('staff', views.staff, name='staff'),
    path('transaction', views.transaction, name='new_transaction'),
]
