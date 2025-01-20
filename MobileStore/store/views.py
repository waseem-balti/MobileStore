from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AccessoryForm, LaptopForm, UserUpdateForm, ProfileUpdateForm
from .forms import CheckoutForm
from django.db import IntegrityError


from .models import (
    MobilePhone, Product, Review, Advertisement, Image, Order, SellerReview, 
    Laptop, Accessory, ShopOwner, PasswordResetToken, Profile, Address, 
    PaymentMethod, Wishlist, Cart, CartItem, OrderItem, Order, OrderItem
)
from .forms import (
    ReviewForm, InquiryForm, MobilePhoneForm, OrderForm, SellerReviewForm, 
    SignupForm, LoginForm, CustomPasswordResetForm, CustomSetPasswordForm
)



@login_required
def orders_list(request):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders,'cart_item_count': cart_item_count,})

@login_required
def order_detail(request, order_id):
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order, 'cart_item_count': cart_item_count})

def cart_count(request):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()

@login_required
def profile(request):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, 
                                       request.FILES, 
                                       instance=request.user.profile)
        if not profile_form.is_valid():
            print(profile_form.errors)
            
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'users/profile.html', context)                

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            # Create reset token
            reset_token = PasswordResetToken.objects.create(user=user)
            
            # Build reset URL
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', args=[str(reset_token.token)])
            )
            
            # Email content
            context = {
                'user': user,
                'reset_url': reset_url,
                'expires_in': '24 hours'
            }
            html_message = render_to_string('password_reset_email.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                'Password Reset Request',
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('login')
            
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    
    return render(request, 'registration/password_reset_form.html')

def password_reset_confirm(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if not reset_token.is_valid:
            messages.error(request, 'This password reset link has expired or been used.')
            return redirect('password_reset_request')
        
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'password_reset_confirm.html')
            
            # Update password
            user = reset_token.user
            user.set_password(password)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            messages.success(request, 'Your password has been successfully reset.')
            return redirect('login')
            
        return render(request, 'password_reset_confirm.html')
        
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid password reset link.')
        return redirect('password_reset_request')


def index(request):
    cart_item_count = 0

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()

    # Fetch phones, ads, laptops, and accessories for display
    phones = MobilePhone.objects.filter(is_available=True)
    ads = Advertisement.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).order_by('-priority')
    laptops = Laptop.objects.all()
    accessories = Accessory.objects.all()

    # Pass the data to the template context
    return render(request, 'index.html', {
        'phones': phones,
        'ads': ads,
        'laptops': laptops,
        'accessories': accessories,
        'cart_item_count': cart_item_count  # Pass the cart item count here
    })

def phone_detail(request, slug):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    phone = get_object_or_404(MobilePhone, slug=slug)
    reviews = phone.reviews.all()
    images = phone.images.all()  # Get all images associated with the phone
    advertisements = Advertisement.objects.filter(mobile_phone=phone, is_active=True)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.user = request.user
                review.mobile_phone = phone
                review.save()
                return redirect('phone_detail', slug=slug)
            else:
                return redirect('login')  # Redirect unauthenticated users to login
    else:
        form = ReviewForm()

    rating_range = range(1, 6)

    return render(request, 'phone_detail.html', {
        'phone': phone, 
        'reviews': reviews, 
        'form': form,
        'rating_range': rating_range,
        'images': images,  # Pass images to template
        'advertisements': advertisements,
        'cart_item_count': cart_item_count
    })




def laptops(request):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    laptops = Laptop.objects.filter(is_available=True)
    return render(request, 'laptops.html', {'laptops': laptops,'cart_item_count' : cart.items.count, 'cart_item_count': cart_item_count})


def accessories(request):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    accessories = Accessory.objects.filter(is_available=True)
    return render(request, 'accessories.html', {'accessories': accessories, 'cart_item_count': cart_item_count})


def laptop_detail(request, slug):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    laptop = get_object_or_404(Laptop, slug=slug)  # Assuming you have a 'slug' field in your Laptop model
    reviews = laptop.reviews.all()  # Assuming there's a related name for reviews in the Laptop model
    rating_range = range(1, 6)

    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.laptop = laptop
            review.user = request.user
            review.save()
            return redirect('laptop_detail', laptop_id=laptop.id)
    
    form = ReviewForm()
    rating_range = range(1, 6)
    return render(request, 'laptop_detail.html', {
        'laptop': laptop,
        'reviews': reviews,
        'form': form,
        'rating_range': rating_range,
        'cart_item_count': cart_item_count,
    })

def accessory_detail(request, slug):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    accessory = get_object_or_404(Accessory, slug=slug)
    reviews = accessory.reviews.all()  # Assuming the related_name for reviews is 'reviews'
    rating_range = range(1, 6)  # For star ratings

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.user = request.user
                review.accessory = accessory
                review.save()
                return redirect('accessory_detail', slug=slug)
            else:
                return redirect('login')  # Redirect unauthenticated users to login
    else:
        form = ReviewForm()

    return render(request, 'accessory_detail.html', {
        'accessory': accessory,
        'reviews': reviews,
        'form': form,
        'rating_range': rating_range,
        'cart_item_count': cart_item_count
    })

def submit_review(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.laptop = laptop
            if request.user.is_authenticated:
                review.user = request.user  # Assign the logged-in user
                review.save()
                return redirect('laptop_detail', slug=laptop.slug)  # Redirect after saving
            else:
                return redirect('login')  # Redirect to login if the user is not authenticated
    else:
        form = ReviewForm()

    return render(request, 'laptop_detail.html', {
        'laptop': laptop,
        'form': form,
    })



def mobile_phone_list(request):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    phones = MobilePhone.objects.all()
    cart_count = request.session.get('cart_count', 0)
    
    context = {
        'phones': phones,
        'cart_count': cart_count,
        'cart_item_count': cart_item_count
    }

    return render(request, 'phones.html', context)

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



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            try:
                Profile.objects.create(user=user)
            except IntegrityError:
                pass  # Profile already exists, ignore the error
            return redirect('index')  # Redirect after signup
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')  # Redirect after login
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout






def create_mobile_phone(request):
    if request.method == 'POST':
        form = MobilePhoneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with the actual redirect
    else:
        form = MobilePhoneForm()
    return render(request, 'create_mobile_phone.html', {'form': form})

def create_laptop(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with the actual redirect
    else:
        form = LaptopForm()
    return render(request, 'create_laptop.html', {'form': form})

def create_accessory(request):
    if request.method == 'POST':
        form = AccessoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with the actual redirect
    else:
        form = AccessoryForm()
    return render(request, 'create_accessory.html', {'form': form})





@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Add or update the cart item
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    # Update cart item count in the session
    cart_item_count = cart.items.count()
    request.session['cart_item_count'] = cart_item_count

    # Redirect to cart view or product page as required
    return redirect('view_cart')  # Replace 'view_cart' with the actual URL name for the cart page

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in items)  # Ensure proper price calculation

    # Pass cart details to the template
    return render(request, 'cart.html', {
        'cart': cart,
        'items': items,
        'total_price': total_price,
        'cart_item_count': request.session.get('cart_item_count', 0)  # Retrieve the cart item count from the session
    })

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')




@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(item.total_price() for item in items)
    cart_item_count = cart.items.count()
    # Ensure cart has items before proceeding
    if not items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')  # Redirect back to the cart if it's empty

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            request.session['address'] = address
            # Proceed with creating the order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_price,
                status='Pending',  # Default order status
                order_number=f"ORD{cart.id}{str(total_price).zfill(4)}"  # Create an order number
            )

            # Create order items for each cart item
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Clear cart items after successful order placement
            cart.items.all().delete()

            # Show success message and redirect to confirmation page
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('order_confirmation', order_id=order.id)

    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form, 'total_price': total_price})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})



@login_required
def get_cart_items(request):
    # Assuming your cart is stored in the session
    cart_items = request.session.get('cart_items', [])
    return cart_items



def product_list(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})