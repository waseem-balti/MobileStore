from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

# User roles for better management
class Role(models.TextChoices):
    SHOP_OWNER = "shop_owner", "Shop Owner"
    CUSTOMER = "customer", "Customer"
    ADMIN = "admin", "Admin"

class ShopOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shop_owner_profile")
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    store_name = models.CharField(max_length=255)
    registration_date = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # Average rating for shop owner

    def __str__(self):
        return self.store_name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    wishlist = models.ManyToManyField('MobilePhone', related_name='wishlisted_by', blank=True)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MobilePhone(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, related_name="mobile_phones")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="mobile_phones")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    # Network Fields
    technology = models.CharField(max_length=255, blank=True, null=True)
    network_bands = models.TextField(blank=True, null=True)

    # Launch Fields
    announcement_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    # Body Fields
    dimensions = models.CharField(max_length=255, blank=True, null=True)
    weight = models.CharField(max_length=255, blank=True, null=True)
    build = models.TextField(blank=True, null=True)
    sim = models.CharField(max_length=255, blank=True, null=True)
    water_resistant = models.BooleanField(default=False)

    # Display Fields
    display_type = models.CharField(max_length=255, blank=True, null=True)
    display_size = models.CharField(max_length=255, blank=True, null=True)
    display_resolution = models.CharField(max_length=255, blank=True, null=True)
    display_protection = models.CharField(max_length=255, blank=True, null=True)

    # Platform Fields
    os = models.CharField(max_length=255, blank=True, null=True)
    chipset = models.CharField(max_length=255, blank=True, null=True)
    cpu = models.CharField(max_length=255, blank=True, null=True)
    gpu = models.CharField(max_length=255, blank=True, null=True)

    # Memory Fields
    card_slot = models.CharField(max_length=255, blank=True, null=True)
    internal_memory = models.CharField(max_length=255, blank=True, null=True)

    # Main Camera Fields
    main_camera = models.TextField(blank=True, null=True)
    camera_features = models.TextField(blank=True, null=True)
    video_capabilities = models.CharField(max_length=255, blank=True, null=True)

    # Selfie Camera Fields
    selfie_camera = models.TextField(blank=True, null=True)
    selfie_video = models.CharField(max_length=255, blank=True, null=True)

    # Sound Fields
    speaker = models.CharField(max_length=255, blank=True, null=True)
    jack_3_5mm = models.BooleanField(default=False)

    # Communication Fields
    wlan = models.CharField(max_length=255, blank=True, null=True)
    bluetooth = models.CharField(max_length=255, blank=True, null=True)
    positioning = models.CharField(max_length=255, blank=True, null=True)
    nfc = models.BooleanField(default=False)
    usb = models.CharField(max_length=255, blank=True, null=True)

    # Features Fields
    sensors = models.TextField(blank=True, null=True)

    # Battery Fields
    battery_type = models.CharField(max_length=255, blank=True, null=True)
    charging = models.TextField(blank=True, null=True)

    # Miscellaneous Fields
    colors = models.TextField(blank=True, null=True)
    price_range = models.CharField(max_length=255, blank=True, null=True)

    # Basic Fields
    storage = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    battery_capacity = models.CharField(max_length=255)
    camera = models.CharField(max_length=255)
    display = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    sim = models.CharField(max_length=255)
    pta_approved = models.BooleanField(default=False)
    five_g_supported = models.BooleanField(default=False)
    fingerprint = models.BooleanField(default=False)
    wifi = models.BooleanField(default=True)
    bluetooth = models.BooleanField(default=True)
    usb_type_c = models.BooleanField(default=True)
    fast_charging = models.BooleanField(default=False)
    fast_wireless_charging = models.BooleanField(default=False)
    reverse_wireless_charging = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.shop_owner.store_name}"

class SellerReview(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, related_name="seller_reviews")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="seller_reviews")
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.user.username} for {self.shop_owner.store_name}"

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ], default="processing")

    def __str__(self):
        return f"Order {self.id} by {self.customer.user.username}"


# Order Items model for line items in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    mobile_phone = models.ForeignKey(MobilePhone, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item: {self.mobile_phone.name} in Order {self.order.id}"

# Notifications for system alerts
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"







class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="transactions")
    mobile_phone = models.ForeignKey(MobilePhone, on_delete=models.SET_NULL, null=True, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=255, choices=[
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
        ("cash", "Cash"),
        ("bank_transfer", "Bank Transfer")
    ])
    status = models.CharField(max_length=50, choices=[
        ("completed", "Completed"),
        ("pending", "Pending"),
        ("cancelled", "Cancelled")
    ], default="pending")

    def __str__(self):
        return f"Transaction by {self.customer.user.username} for {self.mobile_phone.name}"

class Advertisement(models.Model):
    laptop = models.ForeignKey(
        'Laptop',
        related_name='advertisements',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    mobile_phone = models.ForeignKey(
        'MobilePhone',
        related_name='advertisements',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    accessory = models.ForeignKey(
    'Accessory',
    related_name='advertisements',
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, related_name="advertisements")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)  # Higher priority ads can appear at the top

    def __str__(self):
        return f"Ad for {self.mobile_phone.name} by {self.shop_owner.store_name}"

class Inquiry(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="inquiries")
    mobile_phone = models.ForeignKey(MobilePhone, on_delete=models.CASCADE, related_name="inquiries")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.customer.user.username} for {self.mobile_phone.name}"
    


class Tablet(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, related_name="tablets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tablets")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    # Tablet-specific fields
    screen_size = models.CharField(max_length=255, blank=True, null=True)
    operating_system = models.CharField(max_length=255, blank=True, null=True)
    storage = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    battery_capacity = models.CharField(max_length=255)
    camera = models.CharField(max_length=255)
    sim_support = models.CharField(max_length=255, blank=True, null=True)
    
    # Common specifications (can be shared with MobilePhone model)
    display = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    wifi = models.BooleanField(default=True)
    bluetooth = models.BooleanField(default=True)
    usb_type_c = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.shop_owner.store_name}"



class Accessory(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, related_name="accessories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="accessories")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    mobile_phone = models.ForeignKey(MobilePhone, related_name='accessories', on_delete=models.CASCADE, null=True, blank=True)

    # Accessory-specific fields
    type = models.CharField(max_length=255, blank=True, null=True)  # E.g., "Case", "Screen Protector", "Charger"
    compatibility = models.CharField(max_length=255, blank=True, null=True)  # E.g., "For iPhone", "Universal"
    
    # Common specifications (can be shared with MobilePhone model)
    is_available = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.shop_owner.store_name}"


class Laptop(models.Model):
    shop_owner = models.ForeignKey(ShopOwner, on_delete=models.CASCADE, related_name="laptops")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="laptops")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    # Laptop-specific fields
    screen_size = models.CharField(max_length=255, blank=True, null=True)
    operating_system = models.CharField(max_length=255, blank=True, null=True)
    storage = models.CharField(max_length=255)
    ram = models.CharField(max_length=255)
    processor = models.CharField(max_length=255)
    graphics_card = models.CharField(max_length=255, blank=True, null=True)
    battery_life = models.CharField(max_length=255)
    
    # Common specifications (can be shared with MobilePhone model)
    display = models.CharField(max_length=255)
    os = models.CharField(max_length=255)
    wifi = models.BooleanField(default=True)
    bluetooth = models.BooleanField(default=True)
    usb_type_c = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    brand = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.shop_owner.store_name}"


# Image Model Debugging
class Image(models.Model):
    mobile_phone = models.ForeignKey(
        MobilePhone, on_delete=models.CASCADE, related_name="images", blank=True, null=True
    )
    laptop = models.ForeignKey(
        Laptop, on_delete=models.CASCADE, related_name="images", blank=True, null=True
    )
    accessory = models.ForeignKey(
        Accessory, on_delete=models.CASCADE, related_name="images", blank=True, null=True
    )
    image = models.ImageField(
        upload_to="images/",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    is_featured = models.BooleanField(default=False)

    accessory = models.ForeignKey(Accessory, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    laptop = models.ForeignKey(Laptop, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.mobile_phone or self.laptop or self.accessory}"


class Review(models.Model):
    accessory = models.ForeignKey(Accessory, related_name="reviews", on_delete=models.CASCADE, null=True, blank=True)
    laptop = models.ForeignKey(Laptop, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)
    mobile_phone = models.ForeignKey(MobilePhone, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="reviews",  null=True, blank=True)
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        if self.user:
            return f'Review by {self.user.username} for {self.mobile_phone}'
        return 'No user assigned'
    


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('smartphones', 'Smartphones'),
        ('laptops', 'Laptops'),
        ('accessories', 'Accessories'),
        # Add other categories here
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    
    def __str__(self):
        return self.name
