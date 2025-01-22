from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    ShopOwner, Customer, Category, MobilePhone, Laptop, Accessory, Image, Review, 
    Transaction, Advertisement, Inquiry, Profile, Address, PaymentMethod, Wishlist, Order, OrderItem, 
    PasswordResetToken, SellerReview, Notification, Tablet, Cart, CartItem
)
from .forms import CartItemAdminForm

# Inline for Images
class MobilePhoneImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fk_name = "mobile_phone"

class LaptopImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fk_name = "laptop"

class AccessoryImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fk_name = "accessory"

# ShopOwner Admin
@admin.register(ShopOwner)
class ShopOwnerAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'user', 'phone_number', 'rating']
    search_fields = ['store_name', 'user__username']
    ordering = ['-rating']

# Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number']
    search_fields = ['user__username', 'phone_number']
    ordering = ['user__username']

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}
    ordering = ['name']

# MobilePhone Admin
@admin.register(MobilePhone)
class MobilePhoneAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'price', 'shop_owner', 'category', 'is_available', 'pta_approved',
        'five_g_supported', 'created_at', 'updated_at', 'views'
    ]
    list_filter = [
        'is_available', 'five_g_supported', 'pta_approved', 'water_resistant',
        'fast_charging', 'fast_wireless_charging', 'reverse_wireless_charging'
    ]
    search_fields = [
        'name', 'shop_owner__store_name', 'category__name', 'os', 'chipset', 'dimensions'
    ]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['created_at', 'updated_at', 'views']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'shop_owner', 'category', 'price', 'description', 'image')
        }),
        ('Network', {
            'fields': (
                'technology', 'network_bands', 'network_2g_bands', 'network_3g_bands',
                'network_4g_bands', 'network_5g_bands', 'network_speed'
            )
        }),
        ('Launch', {
            'fields': ('announcement_date', 'status')
        }),
        ('Body', {
            'fields': ('dimensions', 'weight', 'sim', 'water_resistant')
        }),
        ('Display', {
            'fields': ('display_type', 'display_size', 'display_resolution', 'display_protection')
        }),
        ('Platform', {
            'fields': ('os', 'chipset', 'cpu', 'gpu')
        }),
        ('Memory', {
            'fields': ('card_slot', 'internal_memory', 'ram')
        }),
        ('Main Camera', {
            'fields': ('main_camera', 'camera_features', 'video_capabilities')
        }),
        ('Selfie Camera', {
            'fields': ('selfie_camera', 'selfie_video')
        }),
        ('Sound', {
            'fields': ('speaker', 'jack_3_5mm')
        }),
        ('Communication', {
            'fields': ('wlan', 'bluetooth', 'positioning', 'nfc', 'usb_type')
        }),
        ('Features', {
            'fields': ('sensors', 'fingerprint', 'wifi')
        }),
        ('Battery', {
            'fields': (
                'battery_type', 'battery_capacity', 'charging', 'fast_charging',
                'fast_wireless_charging', 'reverse_wireless_charging'
            )
        }),
        ('Miscellaneous', {
            'fields': (
                'colors', 'price_range', 'pta_approved', 'five_g_supported',
                'is_available', 'views'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    inlines = [MobilePhoneImageInline]
    ordering = ['-created_at']

# Laptop Admin
@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    # Display important fields in the list view
    list_display = [
        'name', 'price', 'shop_owner', 'is_available', 
        'os', 'brand', 'processor', 'screen_size', 'created_at'
    ]
    # Add filters for easier navigation
    list_filter = [
        'is_available', 'os', 'brand', 'processor_generation', 
        'storage_type', 'touchscreen'
    ]
    # Enable search functionality for relevant fields
    search_fields = [
        'name', 'shop_owner__store_name', 'processor', 
        'graphics_card', 'brand'
    ]
    # Prepopulate the slug field based on the name
    prepopulated_fields = {"slug": ("name",)}
    # Make certain fields read-only
    readonly_fields = ['created_at', 'updated_at']
    # Add inline image functionality if applicable
    inlines = []  # Replace with your image inline if necessary (e.g., LaptopImageInline)
    # Set default ordering
    ordering = ['-created_at']
    # Configure the fieldsets for detailed editing
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "shop_owner", "category", "price", "description", "image")
        }),
        ("Specifications", {
            "fields": (
                "brand", "processor", "processor_generation", "ram", 
                "storage_type", "storage_size", "graphics_card", 
                "screen_size", "display_resolution", "refresh_rate", "touchscreen"
            )
        }),
        ("Connectivity & Features", {
            "fields": ("os", "wifi", "bluetooth", "usb_type_c", "battery_life")
        }),
        ("Status & Metadata", {
            "fields": ("is_available", "views", "created_at", "updated_at")
        }),
    )

    inlines = [LaptopImageInline]
# Accessory Admin
@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'shop_owner', 'is_available', 'created_at']
    list_filter = ['is_available', 'category']
    search_fields = ['name', 'shop_owner__store_name']
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AccessoryImageInline]
    ordering = ['-created_at']

# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['mobile_phone', 'customer', 'rating', 'created_at']
    search_fields = ['mobile_phone__name', 'customer__user__username']
    ordering = ['-created_at']

# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'mobile_phone', 'amount', 'transaction_date', 'status']
    list_filter = ['status']
    search_fields = ['customer__user__username', 'mobile_phone__name']
    ordering = ['-transaction_date']

# Advertisement Admin
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['mobile_phone', 'shop_owner', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active']
    search_fields = ['mobile_phone__name', 'shop_owner__store_name']
    ordering = ['-start_date']

# Inquiry Admin
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['customer', 'mobile_phone', 'created_at']
    search_fields = ['customer__user__username', 'mobile_phone__name']
    ordering = ['-created_at']

# Image Admin
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['mobile_phone', 'laptop', 'accessory', 'image_preview', 'is_featured', 'created_at']
    list_filter = ['is_featured']
    search_fields = ['mobile_phone__name', 'laptop__name', 'accessory__name']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" />')
        return "-"
    image_preview.short_description = 'Image Preview'

# Profile Admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'bio']
    search_fields = ['user__username', 'phone']

# Address Admin
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'city', 'state', 'country', 'postal_code']
    search_fields = ['user__username', 'city', 'state', 'country']

# PaymentMethod Admin
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_number', 'expiry_date', 'cardholder_name']
    search_fields = ['user__username', 'card_number']

# Wishlist Admin
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_name', 'product_category', 'added_at']
    search_fields = ['user__username', 'product_name', 'product_category']

# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_number', 'status', 'total_amount', 'created_at', 'updated_at']
    search_fields = ['user__username', 'order_number']
    list_filter = ['status', 'created_at']

# OrderItem Admin
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'quantity', 'price']
    search_fields = ['order__order_number', 'product__name']

# PasswordResetToken Admin
@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_used', 'expires_at']
    search_fields = ['user__username', 'token']

# SellerReview Admin
@admin.register(SellerReview)
class SellerReviewAdmin(admin.ModelAdmin):
    list_display = ['shop_owner', 'customer', 'rating', 'created_at']
    search_fields = ['shop_owner__name', 'customer__user__username']

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
    search_fields = ['user__username', 'message']

# Tablet Admin
@admin.register(Tablet)
class TabletAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'shop_owner', 'is_available']
    search_fields = ['name', 'category__name', 'shop_owner__name']
    list_filter = ['is_available']

# Cart Admin
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_items', 'total_price_display')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)

    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = 'Total Items'

    def total_price_display(self, obj):
        return f"PKR {obj.total_price():,.2f}"  # Display total price formatted
    total_price_display.short_description = 'Total Price'

# CartItem Admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'get_item_name', 'quantity')
    list_filter = ('cart', 'mobile_phone', 'laptop', 'accessory')

    def get_item_name(self, obj):
        if obj.mobile_phone:
            return obj.mobile_phone.name
        elif obj.laptop:
            return obj.laptop.name
        elif obj.accessory:
            return obj.accessory.name
        return 'Unknown Item'
    get_item_name.short_description = 'Item'