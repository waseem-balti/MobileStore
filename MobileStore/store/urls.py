from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('phone/<slug:slug>/', views.phone_detail, name='phone_detail'),
    path('laptops/', views.laptops, name='laptops'),
    path('laptops/<slug:slug>/', views.laptop_detail, name='laptop_detail'),
    path('accessories/', views.accessories, name='accessories'),
    path('accessories/<slug:slug>/', views.accessory_detail, name='accessory_detail'),
    path('smartphones/', views.smartphones_category, name='smartphones_category'),
    path('laptops/', views.laptops_category, name='laptops_category'),
    path('accessories/', views.accessories_category, name='accessories_category'),
    path('phones/', views.mobile_phone_list, name='phones'),
    path('phones/<slug:slug>/', views.phone_detail, name='phone_detail'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
