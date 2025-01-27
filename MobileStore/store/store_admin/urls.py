from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('shop-owners/', views.manage_shop_owners, name='manage_shop_owners'),
    path('customers/', views.manage_customers, name='manage_customers'),
    path('phones/', views.manage_phones, name='manage_phones'),
    path('carts/', views.manage_carts, name='manage_carts'),
    path('orders/', views.manage_orders, name='manage_orders'),
    path('all-phones/', views.phone_list, name='phone_list'),
    path('phones/create/', views.phone_create, name='phone_create'),
    path('phones/<int:pk>/update/', views.phone_update, name='phone_update'),
    path('phones/<int:pk>/delete/', views.phone_delete, name='phone_delete'),
]