from django import forms
from .models import Address, MobilePhone, Notification, OrderItem, PasswordResetToken, PaymentMethod, Review, Inquiry, Order, SellerReview, Category, ShopOwner, Customer, Advertisement, Image, Laptop, Accessory, Tablet, Transaction, Wishlist, Cart, CartItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'address', 'bio']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 2}),
            'bio': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'})
        }

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['message']

class MobilePhoneForm(forms.ModelForm):
    class Meta:
        model = MobilePhone
        fields = [
            'shop_owner', 'category', 'name', 'price', 'description', 
            'technology', 'network_bands', 'announcement_date', 'status', 
            'dimensions', 'weight', 'sim', 'water_resistant',
            'display_type', 'display_size', 'display_resolution', 
            'display_protection', 'os', 'chipset', 'cpu', 
            'gpu', 'card_slot', 'internal_memory', 'ram', 'main_camera', 
            'camera_features', 'video_capabilities', 
            'selfie_camera', 'selfie_video', 'speaker', 'jack_3_5mm', 
            'wlan', 'bluetooth', 'positioning', 'nfc', 'usb_type', 
            'sensors', 'battery_type', 'battery_capacity', 
            'charging', 'fast_charging', 'fast_wireless_charging', 
            'reverse_wireless_charging', 'colors', 'price_range', 
            'pta_approved', 'five_g_supported', 'fingerprint', 
            'wifi', 'is_available'
        ]



class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = '__all__'
        exclude = ['slug', 'views', 'created_at', 'updated_at']


class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['name', 'price', 'description', 'category', 'shop_owner', 'mobile_phone', 'type', 'compatibility', 
                  'is_available', 'slug']

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True)

class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

# ShopOwner Form
class ShopOwnerForm(forms.ModelForm):
    class Meta:
        model = ShopOwner
        fields = ['store_name', 'user', 'phone_number', 'rating']

# Customer Form
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['user', 'phone_number']

# Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']

# Image Form
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['mobile_phone', 'laptop', 'accessory', 'image', 'is_featured']

# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'hidden peer'}),
            'review_text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full border-2 border-gray-200 rounded-xl p-4 text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none',
                'placeholder': 'Share your experience with this product...'
            }),
        }

    def clean_review_text(self):
        review_text = self.cleaned_data.get('review_text')
        if len(review_text) < 10:
            raise forms.ValidationError('Review text must be at least 10 characters long.')
        return review_text

# Transaction Form
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['customer', 'mobile_phone', 'amount', 'status']

# Advertisement Form
class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['mobile_phone', 'shop_owner', 'start_date', 'end_date', 'is_active']

# Inquiry Form
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['customer', 'mobile_phone', 'message']

# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'phone', 'address', 'bio']

# Address Form
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['user', 'street_address', 'city', 'state', 'country', 'postal_code']

# PaymentMethod Form
class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['user', 'card_number', 'expiry_date', 'cardholder_name']

# Wishlist Form
class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['user', 'product_name', 'product_category']

# Order Form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'order_number', 'status', 'total_amount']

# OrderItem Form
class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'mobile_phone', 'laptop', 'accessory', 'quantity', 'price']

# PasswordResetToken Form
class PasswordResetTokenForm(forms.ModelForm):
    class Meta:
        model = PasswordResetToken
        fields = ['user', 'is_used', 'expires_at']

# SellerReview Form
class SellerReviewForm(forms.ModelForm):
    class Meta:
        model = SellerReview
        fields = ['shop_owner', 'customer', 'rating', 'review_text']

# Notification Form
class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'message', 'is_read']

# Tablet Form
class TabletForm(forms.ModelForm):
    class Meta:
        model = Tablet
        fields = ['name', 'price', 'category', 'shop_owner', 'is_available']

class CartItemAdminForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'mobile_phone', 'laptop', 'accessory', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cart'].queryset = Cart.objects.all()
        self.fields['mobile_phone'].queryset = MobilePhone.objects.all()
        self.fields['laptop'].queryset = Laptop.objects.all()
        self.fields['accessory'].queryset = Accessory.objects.all()

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=255, label='Full Name')
    address = forms.CharField(widget=forms.Textarea, label='Shipping Address')
    phone_number = forms.CharField(max_length=15, label='Phone Number')
    payment_method = forms.ChoiceField(choices=[('cash_on_delivery', 'Cash on Delivery'), ('credit_card', 'Credit Card')], label='Payment Method')