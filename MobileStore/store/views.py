from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import MobilePhone, Product, Review, Advertisement, Image, Order, SellerReview, Laptop, Accessory, ShopOwner
from .forms import ReviewForm, InquiryForm, MobilePhoneForm, OrderForm, SellerReviewForm
from django.http import HttpResponse


def index(request):
    phones = MobilePhone.objects.filter(is_available=True)
    ads = Advertisement.objects.filter(
        is_active=True, 
        start_date__lte=timezone.now(), 
        end_date__gte=timezone.now()
    ).order_by('-priority')
    laptops = Laptop.objects.all()
    accessories = Accessory.objects.all()
    ads = Advertisement.objects.all()
    return render(request, 'index.html', {
        'phones': phones,
        'ads': ads,
        'laptops': laptops,
        'accessories': accessories
    })

def phone_detail(request, slug):
    phone = get_object_or_404(MobilePhone, slug=slug)
    reviews = phone.reviews.all()
    images = phone.images.all()  # Get all images associated with the phone
    advertisements = Advertisement.objects.filter(mobile_phone=phone, is_active=True)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user.customer_profile
            review.mobile_phone = phone
            review.save()
            return redirect('phone_detail', slug=slug)
    else:
        form = ReviewForm()

    rating_range = range(1, 6)
    
    return render(request, 'phone_detail.html', {
        'phone': phone, 
        'reviews': reviews, 
        'form': form,
        'rating_range': rating_range,
        'images': images,  # Pass images to template
        'advertisements': advertisements  # Pass advertisements to template
    })



def laptops(request):
    laptops = Laptop.objects.filter(is_available=True)
    return render(request, 'laptops.html', {'laptops': laptops})

def laptop_detail(request, slug):
    laptop = get_object_or_404(Laptop, slug=slug)  # Assuming you have a 'slug' field in your Laptop model
    reviews = laptop.reviews.all()  # Assuming there's a related name for reviews in the Laptop model
    rating_range = [1, 2, 3, 4, 5]

    return render(request, 'laptop_detail.html', {
        'laptop': laptop,
        'reviews': reviews,
        'rating_range': rating_range,
    })

def accessories(request):
    accessories = Accessory.objects.filter(is_available=True)
    return render(request, 'accessories.html', {'accessories': accessories})


def accessory_detail(request, slug):
    accessory = get_object_or_404(Accessory, slug=slug)
    reviews = Review.objects.filter(accessory=accessory)  # Corrected to filter by accessory
    mobile_phone = accessory.mobile_phone  # Accessory belongs to mobile_phone
    accessories = mobile_phone.accessories.all()  # This will work because of 'related_name'

    rating_range = [1, 2, 3, 4, 5]  # For star ratings

    return render(request, 'accessory_detail.html', {
        'accessories': accessories,
        'accessory': accessory,
        'reviews': reviews,
        'rating_range': rating_range,
    })



def submit_review(request, laptop_id):
    laptop = Laptop.objects.get(id=laptop_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.laptop = laptop
            review.save()
            return redirect('laptop_detail', laptop_id=laptop.id)
    
    else:
        form = ReviewForm()

    return render(request, 'laptop_detail.html', {'laptop': laptop, 'form': form})


def mobile_phone_list(request):
    phones = MobilePhone.objects.all()
    return render(request, 'phones.html', {'phones': phones})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer_profile
            order.save()
            return redirect('order_detail', pk=order.id)
    else:
        form = OrderForm()
    return render(request, 'order_create.html', {'form': form})

def seller_review(request, shop_owner_id):
    shop_owner = ShopOwner.objects.get(id=shop_owner_id)
    if request.method == 'POST':
        form = SellerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user.customer_profile
            review.shop_owner = shop_owner
            review.save()
            return redirect('shop_owner_detail', pk=shop_owner.id)
    else:
        form = SellerReviewForm()
    return render(request, 'seller_review.html', {'form': form, 'shop_owner': shop_owner})



def smartphones_category(request):
    products = Product.objects.filter(category='smartphones')
    return render(request, 'category_page.html', {'category_name': 'Smartphones', 'products': products})

def laptops_category(request):
    products = Product.objects.filter(category='laptops')
    return render(request, 'category_page.html', {'category_name': 'Laptops', 'products': products})

def accessories_category(request):
    products = Product.objects.filter(category='accessories')
    return render(request, 'category_page.html', {'category_name': 'Accessories', 'products': products})
