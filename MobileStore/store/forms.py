from django import forms
from .models import MobilePhone, Review, Inquiry, Order, SellerReview

class MobilePhoneForm(forms.ModelForm):
    class Meta:
        model = MobilePhone
        fields = '__all__'

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
        fields = ['name', 'price', 'description', 'category', 'technology', 'network_bands', 
                  'announcement_date', 'status', 'dimensions', 'weight', 'build', 'sim', 'water_resistant',
                  'display_type', 'display_size', 'display_resolution', 'display_protection', 'os', 'chipset', 'cpu',
                  'gpu', 'card_slot', 'internal_memory', 'main_camera', 'camera_features', 'video_capabilities',
                  'selfie_camera', 'selfie_video', 'speaker', 'jack_3_5mm', 'wlan', 'bluetooth', 'positioning', 'nfc',
                  'usb', 'sensors', 'battery_type', 'charging', 'colors', 'price_range', 'storage', 'ram', 'battery_capacity', 
                  'camera', 'display', 'os', 'sim', 'pta_approved', 'five_g_supported', 'fingerprint', 'wifi', 'bluetooth',
                  'usb_type_c', 'fast_charging', 'fast_wireless_charging', 'reverse_wireless_charging', 'is_available']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_amount', 'status']

class SellerReviewForm(forms.ModelForm):
    class Meta:
        model = SellerReview
        fields = ['rating', 'review_text']
