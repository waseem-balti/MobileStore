from django.shortcuts import render, get_object_or_404, redirect
from store.models import ShopOwner, Customer, MobilePhone, Laptop, Accessory, Cart, CartItem
from .forms import ShopOwnerForm, CustomerForm, MobilePhoneForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.contrib import messages
from store.models import MobilePhone

def admin_dashboard(request):
    return render(request, 'admin/admin_base.html')

def manage_shop_owners(request):
    shop_owners = ShopOwner.objects.all()
    if request.method == 'POST':
        form = ShopOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_shop_owners')
    else:
        form = ShopOwnerForm()
    return render(request, 'admin/manage_shop_owners.html', {'shop_owners': shop_owners, 'form': form})

def manage_customers(request):
    customers = Customer.objects.all()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_customers')
    else:
        form = CustomerForm()
    return render(request, 'admin/manage_customers.html', {'customers': customers, 'form': form})

def manage_phones(request):
    products = MobilePhone.objects.all()  # Extend this for other product types like Laptop, Accessory
    if request.method == 'POST':
        form = MobilePhoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = MobilePhoneForm()
    return render(request, 'admin/manage_phones.html', {'products': products, 'form': form})


def manage_carts(request):
    context = {
        'carts': Cart.objects.all(),
        'customers': Customer.objects.all(),

    }
    return render(request, 'admin/manage_carts.html', context)
   

def manage_orders(request):
    # Implement logic to manage orders
    pass




def phone_list(request):
    phones = MobilePhone.objects.all()
    return render(request, 'admin/phone_list.html', {'phones': phones})

def phone_create(request):
    if request.method == 'POST':
        form = MobilePhoneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Phone created successfully.')
            return redirect('phone_list')
        else:
            messages.error(request, 'Error creating phone.')
    else:
        form = MobilePhoneForm()
    return render(request, 'admin/phone_form.html', {'form': form})

def phone_update(request, pk):
    phone = get_object_or_404(MobilePhone, pk=pk)
    if request.method == 'POST':
        form = MobilePhoneForm(request.POST, request.FILES, instance=phone)
        if form.is_valid():
            form.save()
            messages.success(request, 'Phone updated successfully.')
            return redirect('phone_list')
        else:
            messages.error(request, 'Error updating phone.')
    else:
        form = MobilePhoneForm(instance=phone)
    return render(request, 'admin/phone_form.html', {'form': form})

def phone_delete(request, pk):
    phone = get_object_or_404(MobilePhone, pk=pk)
    if request.method == 'POST':
        phone.delete()
        messages.success(request, 'Phone deleted successfully.')
        return redirect('phone_list')
    return render(request, 'admin/phone_confirm_delete.html', {'phone': phone})