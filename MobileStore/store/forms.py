from django import forms
from .models import MobilePhone, Review, Inquiry, Order, SellerReview, Category, ShopOwner, Customer, Advertisement, Image, Laptop, Accessory, Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone', 'address', 'bio']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']

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
        fields = ['name', 'price', 'description', 'category', 'shop_owner', 'screen_size', 'operating_system', 
                  'storage', 'ram', 'processor', 'graphics_card', 'battery_life', 'display', 'os', 'wifi', 'bluetooth', 
                  'usb_type_c', 'is_available', 'slug', 'brand']
        

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = ['name', 'price', 'description', 'category', 'shop_owner', 'mobile_phone', 'type', 'compatibility', 
                  'is_available', 'slug']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_amount', 'status']

class SellerReviewForm(forms.ModelForm):
    class Meta:
        model = SellerReview
        fields = ['rating', 'review_text']




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


