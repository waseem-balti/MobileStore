from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import (
    signup_view,
    login_view,
    logout_view,
    password_reset_confirm,
    password_reset_request,
)


urlpatterns = [
    path("", views.index, name="index"),
    path("phone/<slug:slug>/", views.phone_detail, name="phone_detail"),
    path("laptops/", views.laptops, name="laptops"),
    path("laptops/<slug:slug>/", views.laptop_detail, name="laptop_detail"),
    path("accessories/", views.accessories, name="accessories"),
    path("accessories/<slug:slug>/", views.accessory_detail, name="accessory_detail"),
    path("smartphones/", views.smartphones_category, name="smartphones_category"),
    path("laptops/", views.laptops_category, name="laptops_category"),
    path("accessories/", views.accessories_category, name="accessories_category"),
    path("phones/", views.mobile_phone_list, name="phones"),
    path("phones/<slug:slug>/", views.phone_detail, name="phone_detail"),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("password_reset_done/",auth_views.PasswordResetDoneView.as_view(),name="password_reset_done",),
    path("password_reset_complete/",auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete",),
    path("password_reset/", views.password_reset_request, name="password_reset_request"),
    path("password_reset/confirm/<str:token>/",views.password_reset_confirm,name="password_reset_confirm",),
    path("profile/", views.profile, name="profile"),
    path("password-change/",auth_views.PasswordChangeView.as_view(template_name="users/password_change.html"),name="password_change",),
    path("password-change/done/",auth_views.PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),name="password_change_done",),
    path('orders/', views.orders_list, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/mobile-phone/', views.create_mobile_phone, name='create_mobile_phone'),
    path('create/laptop/', views.create_laptop, name='create_laptop'),
    path('create/accessory/', views.create_accessory, name='create_accessory'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path("product/<int:product_id>/add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path('products/', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('products/', views.product_list, name='product_list'),

    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
