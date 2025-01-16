from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    ShopOwner, Customer, Category, MobilePhone, Laptop, Accessory, Image, Review, 
    Transaction, Advertisement, Inquiry
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
    extra = 1  # Added extra = 1 for consistency in UI behavior
    fk_name = "accessory"


# ShopOwner Admin
@admin.register(ShopOwner)
class ShopOwnerAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'user', 'phone_number', 'rating']
    search_fields = ['store_name', 'user__username']

# Customer Admin
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number']
    search_fields = ['user__username', 'phone_number']

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}

# MobilePhone Admin
@admin.register(MobilePhone)
class MobilePhoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'shop_owner', 'is_available']
    list_filter = ['is_available', 'five_g_supported', 'pta_approved']
    search_fields = ['name', 'shop_owner__store_name']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MobilePhoneImageInline]

# Laptop Admin
@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'shop_owner', 'is_available']
    list_filter = ['is_available', 'os']
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ['name', 'shop_owner__store_name']
    inlines = [LaptopImageInline]

# Accessory Admin
@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'shop_owner', 'is_available']
    list_filter = ['is_available', 'category']
    search_fields = ['name', 'shop_owner__store_name']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AccessoryImageInline]

# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['mobile_phone', 'customer', 'rating', 'created_at']
    search_fields = ['mobile_phone__name', 'customer__user__username']

# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'mobile_phone', 'amount', 'transaction_date', 'status']
    list_filter = ['status']
    search_fields = ['customer__user__username', 'mobile_phone__name']

# Advertisement Admin
@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['mobile_phone', 'shop_owner', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active']
    search_fields = ['mobile_phone__name', 'shop_owner__store_name']

# Inquiry Admin
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['customer', 'mobile_phone', 'created_at']
    search_fields = ['customer__user__username', 'mobile_phone__name']

# Image Admin
class ImageAdmin(admin.ModelAdmin):
    list_display = ['mobile_phone', 'laptop', 'accessory', 'image_preview', 'is_featured']  # Added accessory here
    list_filter = ['is_featured']
    search_fields = ['mobile_phone__name', 'laptop__name', 'accessory__name']  # Also searching for accessory names
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" />')
        return "-"
    image_preview.short_description = 'Image Preview'

