# Generated by Django 5.1.5 on 2025-01-16 11:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_advertisement_laptop_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='accessory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='advertisements', to='store.accessory'),
        ),
    ]
