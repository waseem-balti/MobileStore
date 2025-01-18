from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    ShopOwner, Customer, Category, MobilePhone, Laptop, Accessory, Image, Review, 
    Transaction, Advertisement, Inquiry,Profile, Address, PaymentMethod, Wishlist, Order, OrderItem, 
    PasswordResetToken, ShopOwner, Customer, Category, MobilePhone, 
    SellerReview, Notification, Transaction, Advertisement, Inquiry, Tablet,
    Image
)

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
    list_display = ['name', 'price', 'shop_owner', 'is_available', 'created_at']
    list_filter = ['is_available', 'five_g_supported', 'pta_approved']
    search_fields = ['name', 'shop_owner__store_name']
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MobilePhoneImageInline]
    ordering = ['-created_at']

# Laptop Admin
@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'shop_owner', 'is_available', 'created_at']
    list_filter = ['is_available', 'os']
    search_fields = ['name', 'shop_owner__store_name']
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LaptopImageInline]
    ordering = ['-created_at']

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

# Custom Admin Actions
@admin.action(description='Mark selected items as featured')
def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)

# Register Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'bio']
    search_fields = ['user__username', 'phone']

# Register Address model
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'city', 'state', 'country', 'postal_code']
    search_fields = ['user__username', 'city', 'state', 'country']

# Register PaymentMethod model
@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_number', 'expiry_date', 'cardholder_name']
    search_fields = ['user__username', 'card_number']

# Register Wishlist model
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_name', 'product_category', 'added_at']
    search_fields = ['user__username', 'product_name', 'product_category']

# Register Order and OrderItem models
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_number', 'status', 'total_amount', 'created_at', 'updated_at']
    search_fields = ['user__username', 'order_number']
    list_filter = ['status', 'created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__order_number', 'product__name']

# Register PasswordResetToken model
@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'is_used', 'expires_at']
    search_fields = ['user__username', 'token']

# Register SellerReview model
@admin.register(SellerReview)
class SellerReviewAdmin(admin.ModelAdmin):
    list_display = ['shop_owner', 'customer', 'rating', 'created_at']
    search_fields = ['shop_owner__name', 'customer__user__username']

# Register Notification model
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
    search_fields = ['user__username', 'message']

# Register Tablet model
@admin.register(Tablet)
class TabletAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'shop_owner', 'is_available']
    search_fields = ['name', 'category__name', 'shop_owner__name']
    list_filter = ['is_available']
