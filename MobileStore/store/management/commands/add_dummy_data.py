import os
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from store.models import MobilePhone, Laptop, Accessory, Image, ShopOwner

class Command(BaseCommand):
    help = "Add dummy items to MobilePhone, Laptop, and Accessory models"

    def download_image(self, url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            return ContentFile(response.content, filename)
        return None

    def handle(self, *args, **kwargs):
        # Define the image URL
        image_url = "https://cdn.pixabay.com/photo/2021/11/16/15/35/electronics-6801339_1280.jpg"

        # Get the first shop owner
        shop_owner = ShopOwner.objects.first()
        if not shop_owner:
            self.stdout.write(self.style.ERROR("No ShopOwner found. Add a ShopOwner first."))
            return

        # Add dummy items to MobilePhone
        for i in range(1, 6):
            mobile = MobilePhone.objects.create(
                name=f"Dummy Mobile {i}",
                price=10000 + i * 500,
                shop_owner=shop_owner,
                is_available=True,
            )
            image_file = self.download_image(image_url, f"mobile_{i}.jpg")
            if image_file:
                Image.objects.create(mobile_phone=mobile, image=image_file)

        # Add dummy items to Laptop
        for i in range(1, 6):
            laptop = Laptop.objects.create(
                name=f"Dummy Laptop {i}",
                price=50000 + i * 1000,
                shop_owner=shop_owner,
                is_available=True,
            )
            image_file = self.download_image(image_url, f"laptop_{i}.jpg")
            if image_file:
                Image.objects.create(laptop=laptop, image=image_file)

        # Add dummy items to Accessory
        for i in range(1, 6):
            accessory = Accessory.objects.create(
                name=f"Dummy Accessory {i}",
                price=500 + i * 50,
                shop_owner=shop_owner,
                is_available=True,
            )
            image_file = self.download_image(image_url, f"accessory_{i}.jpg")
            if image_file:
                Image.objects.create(accessory=accessory, image=image_file)

        self.stdout.write(self.style.SUCCESS("5 dummy items added to each category successfully!"))
