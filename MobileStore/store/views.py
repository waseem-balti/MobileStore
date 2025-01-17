from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import MobilePhone, Product, Review, Advertisement, Image, Order, SellerReview, Laptop, Accessory, ShopOwner
from .forms import ReviewForm, InquiryForm, MobilePhoneForm, OrderForm, SellerReviewForm
from django.http import HttpResponse


def product_detail(request, model, slug, template_name):
    product = get_object_or_404(model, slug=slug)
    reviews = product.reviews.all()
    images = product.images.all()
    advertisements = Advertisement.objects.filter(
        is_active=True,
        **{f"{model.__name__.lower()}": product}
    )

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.user = request.user
                setattr(review, model.__name__.lower(), product)
                review.save()
                return redirect(request.path_info)
            else:
                return redirect('login')
    else:
        form = ReviewForm()

    return render(request, template_name, {
        'product': product,
        'reviews': reviews,
        'form': form,
        'images': images,
        'advertisements': advertisements,
        'rating_range': range(1, 6),
    })


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


def laptops(request):
    laptops = Laptop.objects.filter(is_available=True)
    return render(request, 'laptops.html', {'laptops': laptops})

def accessories(request):
    accessories = Accessory.objects.filter(is_available=True)
    return render(request, 'accessories.html', {'accessories': accessories})


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
            review.user = request.user
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



def phone_detail(request, slug):
    return product_detail(request, MobilePhone, slug, 'phone_detail.html')

def laptop_detail(request, slug):
    return product_detail(request, Laptop, slug, 'laptop_detail.html')

def accessory_detail(request, slug):
    return product_detail(request, Accessory, slug, 'accessory_detail.html')
