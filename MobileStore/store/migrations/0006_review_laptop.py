# Generated by Django 5.1.5 on 2025-01-16 06:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_image_accessory_image_laptop_laptop_brand_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='laptop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.laptop'),
            preserve_default=False,
        ),
    ]
