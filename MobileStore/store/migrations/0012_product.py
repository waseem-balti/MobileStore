# Generated by Django 5.1.5 on 2025-01-16 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_accessory_mobile_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='products/')),
                ('category', models.CharField(choices=[('smartphones', 'Smartphones'), ('laptops', 'Laptops'), ('accessories', 'Accessories')], max_length=50)),
            ],
        ),
    ]
