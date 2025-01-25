import uuid
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
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from fuzzywuzzy import fuzz, process
from difflib import SequenceMatcher
from django.http import Http404


from .models import (
    MobilePhone,
    Review,
    Advertisement,
    Image,
    Order,
    SellerReview,
    Laptop,
    Accessory,
    ShopOwner,
    PasswordResetToken,
    Profile,
    Address,
    PaymentMethod,
    Wishlist,
    Cart,
    CartItem,
    OrderItem,
    Order,
)
from .forms import (
    ReviewForm,
    InquiryForm,
    MobilePhoneForm,
    OrderForm,
    SellerReviewForm,
    SignupForm,
    LoginForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
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
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(
        request,
        "store/orders.html",
        {
            "orders": orders,
            "cart_item_count": cart_item_count,
        },
    )


@login_required
def order_detail(request, order_id):
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(
        request,
        "store/order_detail.html",
        {"order": order, "cart_item_count": cart_item_count},
    )


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
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    cart_item_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_item_count = cart.items.count()

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "cart_item_count": cart_item_count,
    }
    return render(request, "users/profile.html", context)


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)

            # Create reset token
            reset_token = PasswordResetToken.objects.create(user=user)

            # Build reset URL
            reset_url = request.build_absolute_uri(
                reverse("password_reset_confirm", args=[str(reset_token.token)])
            )

            # Email content
            context = {"user": user, "reset_url": reset_url, "expires_in": "24 hours"}
            html_message = render_to_string("password_reset_email.html", context)
            plain_message = strip_tags(html_message)

            # Send email
            send_mail(
                "Password Reset Request",
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )

            messages.success(
                request, "Password reset link has been sent to your email."
            )
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "No user found with this email address.")

    return render(request, "registration/password_reset_form.html")


def password_reset_confirm(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token)

        if not reset_token.is_valid:
            messages.error(
                request, "This password reset link has expired or been used."
            )
            return redirect("password_reset_request")

        if request.method == "POST":
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "password_reset_confirm.html")

            # Update password
            user = reset_token.user
            user.set_password(password)
            user.save()

            # Mark token as used
            reset_token.is_used = True
            reset_token.save()

            messages.success(request, "Your password has been successfully reset.")
            return redirect("login")

        return render(request, "password_reset_confirm.html")

    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid password reset link.")
        return redirect("password_reset_request")


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
        is_active=True, start_date__lte=timezone.now(), end_date__gte=timezone.now()
    ).order_by("-priority")
    laptops = Laptop.objects.all()
    accessories = Accessory.objects.all()

    # Pass the data to the template context
    return render(
        request,
        "index.html",
        {
            "phones": phones,
            "ads": ads,
            "laptops": laptops,
            "accessories": accessories,
            "cart_item_count": cart_item_count,  # Pass the cart item count here
        },
    )


def laptops(request):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()

    laptops = Laptop.objects.filter(is_available=True)

    # Handle form submission
    if request.method == "POST":
        form = LaptopForm(request.POST, request.FILES)  # Include files for image upload
        if form.is_valid():
            form.save()
            return redirect("laptops")  # Redirect to the laptops page after saving
    else:
        form = LaptopForm()

    return render(
        request,
        "laptops.html",
        {
            "laptops": laptops,
            "cart_item_count": cart_item_count,
            "form": form,
        },
    )


def accessories(request):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    accessories = Accessory.objects.filter(is_available=True)
    return render(
        request,
        "accessories.html",
        {"accessories": accessories, "cart_item_count": cart_item_count},
    )


@login_required
def phone_detail(request, slug):
    phone = get_object_or_404(MobilePhone, slug=slug)
    reviews = phone.reviews.all()
    images = phone.images.all()
    advertisements = Advertisement.objects.filter(mobile_phone=phone, is_active=True)
    cart_item_count = 0

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()

    user_reviews = reviews.filter(user=request.user)  # Get reviews by the logged-in user
    user_review_count = user_reviews.count()

    if request.method == "POST":
        # Handling creating or updating a review
        review_id = request.POST.get("review_id")
        if review_id:  # If review ID is present, update the review
            review = get_object_or_404(Review, id=review_id, user=request.user)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, "Your review has been updated successfully!")
                return redirect("phone_detail", slug=slug)
        else:  # If review ID is not present, handle a new review submission
            if user_review_count >= 3:
                messages.error(request, "You can only post 3 reviews. Please edit or delete an existing review to post more.")
                return redirect("phone_detail", slug=slug)

            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.mobile_phone = phone
                review.save()
                messages.success(request, "Your review has been posted successfully!")
                return redirect("phone_detail", slug=slug)
    else:
        form = ReviewForm()

    rating_range = range(1, 6)
    
    # Check for any review deletion request
    if request.method == "GET" and "delete_review_id" in request.GET:
        review_id = request.GET.get("delete_review_id")
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
        messages.success(request, "Your review has been deleted successfully!")
        return redirect("phone_detail", slug=slug)

    return render(
        request,
        "phone_detail.html",
        {
            "phone": phone,
            "reviews": reviews,
            "form": form,
            "rating_range": rating_range,
            "images": images,
            "advertisements": advertisements,
            "cart_item_count": cart_item_count,
            "user_reviews": user_reviews,
            "user_review_count": user_review_count,
        },
    )

@login_required
def laptop_detail(request, slug):
    laptop = get_object_or_404(Laptop, slug=slug)
    reviews = laptop.reviews.all()
    cart_item_count = 0

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.laptop = laptop
            review.save()
            messages.success(request, "Your review has been posted successfully!")
            return redirect("laptop_detail", slug=slug)
    else:
        form = ReviewForm()

    rating_range = range(1, 6)
    return render(
        request,
        "laptop_detail.html",
        {
            "laptop": laptop,
            "reviews": reviews,
            "form": form,
            "rating_range": rating_range,
            "cart_item_count": cart_item_count,
        },
    )


@login_required
def accessory_detail(request, slug):
    accessory = get_object_or_404(Accessory, slug=slug)
    reviews = accessory.reviews.all()
    cart_item_count = 0

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.accessory = accessory
            review.save()
            messages.success(request, "Your review has been posted successfully!")
            return redirect("accessory_detail", slug=slug)
    else:
        form = ReviewForm()

    rating_range = range(1, 6)
    return render(
        request,
        "accessory_detail.html",
        {
            "accessory": accessory,
            "reviews": reviews,
            "form": form,
            "rating_range": rating_range,
            "cart_item_count": cart_item_count,
        },
    )


def submit_review(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.laptop = laptop
            if request.user.is_authenticated:
                review.user = request.user  # Assign the logged-in user
                review.save()
                return redirect(
                    "laptop_detail", slug=laptop.slug
                )  # Redirect after saving
            else:
                return redirect(
                    "login"
                )  # Redirect to login if the user is not authenticated
    else:
        form = ReviewForm()

    return render(
        request,
        "laptop_detail.html",
        {
            "laptop": laptop,
            "form": form,
        },
    )


def mobile_phone_list(request):
    cart_item_count = 0
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Update the cart item count
        cart_item_count = cart.items.count()
    phones = MobilePhone.objects.all()
    cart_count = request.session.get("cart_count", 0)

    context = {
        "phones": phones,
        "cart_count": cart_count,
        "cart_item_count": cart_item_count,
    }

    return render(request, "phones.html", context)


def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user.customer_profile
            order.save()
            return redirect("order_detail", pk=order.id)
    else:
        form = OrderForm()
    return render(request, "order_create.html", {"form": form})


def seller_review(request, shop_owner_id):
    shop_owner = ShopOwner.objects.get(id=shop_owner_id)
    if request.method == "POST":
        form = SellerReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.shop_owner = shop_owner
            review.save()
            return redirect("shop_owner_detail", pk=shop_owner.id)
    else:
        form = SellerReviewForm()
    return render(
        request, "seller_review.html", {"form": form, "shop_owner": shop_owner}
    )


def smartphones_category(request):
    phone = MobilePhone.objects.filter(category="smartphones")
    return render(
        request, "category_page.html", {"category_name": "Smartphones", "phone": phone}
    )


def laptops_category(request):
    laptop = Laptop.objects.filter(category="laptops")
    return render(
        request, "category_page.html", {"category_name": "Laptops", "laptop": laptop}
    )


def accessories_category(request):
    accessory = Accessory.objects.filter(category="accessories")
    return render(
        request,
        "category_page.html",
        {"category_name": "Accessories", "accessory": accessory},
    )


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            try:
                Profile.objects.create(user=user)
            except IntegrityError:
                pass  # Profile already exists, ignore the error
            return redirect("index")  # Redirect after signup
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")  # Redirect after login
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout


def create_mobile_phone(request):
    if request.method == "POST":
        form = MobilePhoneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success_url")  # Replace with the actual redirect
    else:
        form = MobilePhoneForm()
    return render(request, "create_mobile_phone.html", {"form": form})


def create_laptop(request):
    if request.method == "POST":
        form = LaptopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success_url")  # Replace with the actual redirect
    else:
        form = LaptopForm()
    return render(request, "create_laptop.html", {"form": form})


def create_accessory(request):
    if request.method == "POST":
        form = AccessoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success_url")  # Replace with the actual redirect
    else:
        form = AccessoryForm()
    return render(request, "create_accessory.html", {"form": form})


@login_required
def add_to_cart(request, item_type, item_id):
    if item_type == "phone":
        item = get_object_or_404(MobilePhone, id=item_id)
    elif item_type == "laptop":
        item = get_object_or_404(Laptop, id=item_id)
    elif item_type == "accessory":
        item = get_object_or_404(Accessory, id=item_id)
    else:
        return redirect("view_cart")  # Invalid item type

    cart, created = Cart.objects.get_or_create(user=request.user)

    # Add or update the cart item
    if item_type == "phone":
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, mobile_phone=item
        )
    elif item_type == "laptop":
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, laptop=item)
    elif item_type == "accessory":
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, accessory=item
        )

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    # Update cart item count in the session
    cart_item_count = cart.items.count()
    request.session["cart_item_count"] = cart_item_count

    # Redirect to cart view or product page as required
    return redirect(
        "view_cart"
    )  # Replace 'view_cart' with the actual URL name for the cart page


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(
        item.total_price() for item in items
    )  # Ensure proper price calculation

    # Pass cart details to the template
    return render(
        request,
        "cart.html",
        {
            "cart": cart,
            "items": items,
            "total_price": total_price,
            "cart_item_count": request.session.get(
                "cart_item_count", 0
            ),  # Retrieve the cart item count from the session
        },
    )


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

    return redirect("view_cart")


@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("view_cart")



@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(item.total_price() for item in items)
    cart_item_count = cart.items.count()

    # Ensure cart has items before proceeding
    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")  # Redirect back to the cart if it's empty

    profile = request.user.profile  # Get the logged-in user's profile

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data["address"]
            request.session["address"] = address
            # Generate a unique order number
            order_number = f"ORD{uuid.uuid4().hex[:10].upper()}"
            # Proceed with creating the order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_price,
                status="Pending",
                order_number=order_number,
                shipping_address=address, 
            )

            # Create order items for each cart item
            for item in items:
                product = item.get_item()
                if isinstance(product, MobilePhone):
                    OrderItem.objects.create(
                        order=order,
                        mobile_phone=product,
                        quantity=item.quantity,
                        price=product.price,
                    )
                elif isinstance(product, Laptop):
                    OrderItem.objects.create(
                        order=order,
                        laptop=product,
                        quantity=item.quantity,
                        price=product.price,
                    )
                elif isinstance(product, Accessory):
                    OrderItem.objects.create(
                        order=order,
                        accessory=product,
                        quantity=item.quantity,
                        price=product.price,
                    )

            # Clear cart items after successful order placement
            cart.items.all().delete()

            # Show success message and redirect to confirmation page
            messages.success(request, "Your order has been placed successfully!")
            return redirect("order_confirmation", order_id=order.id)

    else:
        # Pass profile data to pre-fill the form fields
        form = CheckoutForm(initial={
            'full_name': request.user.get_full_name(),
            'phone_number': profile.phone,
            'address': profile.address,
        })

    return render(request, "checkout.html", {"form": form, "total_price": total_price})



@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_confirmation.html", {"order": order})


@login_required
def get_cart_items(request):
    # Assuming your cart is stored in the session
    cart_items = request.session.get("cart_items", [])
    return cart_items


def product_list(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item_count = cart.items.count()

    # You can filter products by category
    category_filter = request.GET.get("category", None)
    if category_filter:
        products = MobilePhone.objects.filter(category=category_filter)
    else:
        products = MobilePhone.objects.all()

    return render(
        request,
        "product_list.html",
        {
            "products": products,
            "cart_item_count": cart_item_count,
        },
    )


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all().select_related("mobile_phone", "laptop", "accessory")

    total_price = sum(item.get_total_price() for item in cart_items)

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total_price": total_price,
        },
    )


@login_required
@require_POST
def add_review(request, slug):
    accessory = get_object_or_404(Accessory, slug=slug)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.accessory = accessory
        review.save()
        return JsonResponse(
            {
                "success": True,
                "review": {
                    "user": review.user.username,
                    "created_at": review.created_at.strftime("%b %d, %Y"),
                    "rating": review.rating,
                    "review_text": review.review_text,
                },
            }
        )
    else:
        return JsonResponse({"success": False, "errors": form.errors})






def similar(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def search(request):
    query = request.GET.get('q', '').strip()
    phones, laptops, accessories = [], [], []
    SIMILARITY_THRESHOLD = 0.4 if len(query) <= 3 else 0.6 # Adjust this value to control match sensitivity

    if query:
        # Get all items
        all_phones = MobilePhone.objects.all()
        all_laptops = Laptop.objects.all()
        all_accessories = Accessory.objects.all()

        # Fuzzy search implementation
        for phone in all_phones:
            # Check name similarity
            name_similarity = similar(query, phone.name)
            # Check description words
            desc_words = phone.description.split()
            desc_similarity = max([similar(query, word) for word in desc_words], default=0)
            
            if name_similarity > SIMILARITY_THRESHOLD or desc_similarity > SIMILARITY_THRESHOLD:
                phones.append(phone)

        for laptop in all_laptops:
            name_similarity = similar(query, laptop.name)
            desc_words = laptop.description.split()
            desc_similarity = max([similar(query, word) for word in desc_words], default=0)
            
            if name_similarity > SIMILARITY_THRESHOLD or desc_similarity > SIMILARITY_THRESHOLD:
                laptops.append(laptop)

        for accessory in all_accessories:
            name_similarity = similar(query, accessory.name)
            if accessory.description:  # Check if description exists
                desc_words = accessory.description.split()
                desc_similarity = max([similar(query, word) for word in desc_words], default=0)
            else:
                desc_similarity = 0
            
            if name_similarity > SIMILARITY_THRESHOLD or desc_similarity > SIMILARITY_THRESHOLD:
                accessories.append(accessory)

    context = {
        'query': query,
        'results': {
            'Phone': phones,
            'Laptop': laptops,
            'Accessory': accessories,
        },
        'total_results': len(phones) + len(laptops) + len(accessories),
    }
    return render(request, 'search_results.html', context)


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Add logic to handle newsletter signup
        messages.success(request, 'Successfully subscribed!')
    return redirect('home')











def compare_phones(request):
    # Get the list of phone IDs from the request
    phone_ids = request.GET.getlist('phone')

    if not phone_ids:
        # If no phone IDs are provided, raise a 404 or handle accordingly
        raise Http404("No phones selected for comparison.")

    # Filter phones based on the provided IDs
    phones = MobilePhone.objects.filter(id__in=phone_ids)

    if not phones.exists():
        # If no phones match the given IDs, raise a 404 or handle accordingly
        raise Http404("No matching phones found for comparison.")

    # Render the comparison template with the list of phones
    return render(request, 'compare_phones.html', {'phones': phones})



def search_phones(request):
    query = request.GET.get('q', '')
    phones = MobilePhone.objects.filter(name__icontains=query).prefetch_related('images')
    data = [{
        'id': phone.id,
        'name': phone.name,
        'price': phone.price,
        'images': [{'image': img.image.url} for img in phone.images.all()]
    } for phone in phones]
    return JsonResponse(data, safe=False)

def search_laptops(request):
    query = request.GET.get('q', '')
    laptops = Laptop.objects.filter(name__icontains=query).prefetch_related('images')
    data = [{
        'id': laptop.id,
        'name': laptop.name,
        'price': laptop.price,
        'images': [{'image': img.image.url} for img in laptop.images.all()]
    } for laptop in laptops]
    return JsonResponse(data, safe=False)

def search_accessories(request):
    query = request.GET.get('q', '')
    accessories = Accessory.objects.filter(name__icontains=query).prefetch_related('images')
    data = [{
        'id': acc.id,
        'name': acc.name,
        'price': acc.price,
        'images': [{'image': img.image.url} for img in acc.images.all()]
    } for acc in accessories]
    return JsonResponse(data, safe=False)

def compare_laptops(request):
    laptop_ids = request.GET.getlist('laptop')
    laptops = Laptop.objects.filter(id__in=laptop_ids)
    return render(request, 'compare_laptops.html', {'laptops': laptops})

def compare_accessories(request):
    accessory_ids = request.GET.getlist('accessory')
    accessories = Accessory.objects.filter(id__in=accessory_ids)
    return render(request, 'compare_accessories.html', {'accessories': accessories})