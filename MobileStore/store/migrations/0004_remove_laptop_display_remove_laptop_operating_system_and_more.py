# Generated by Django 5.1.5 on 2025-01-22 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_mobilephone_network_2g_bands_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="laptop",
            name="display",
        ),
        migrations.RemoveField(
            model_name="laptop",
            name="operating_system",
        ),
        migrations.RemoveField(
            model_name="laptop",
            name="storage",
        ),
        migrations.AddField(
            model_name="laptop",
            name="audio_features",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="backlit_keyboard",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="laptop",
            name="battery_type",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="card_reader",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="laptop",
            name="color_options",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="dimensions",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="display_resolution",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="display_type",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="ethernet_port",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="laptop",
            name="fast_charging",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="laptop",
            name="fingerprint_reader",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="laptop",
            name="graphics_memory",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="hdmi_port",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="headphone_jack",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="material",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="processor_generation",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="refresh_rate",
            field=models.IntegerField(blank=True, default=60, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="storage_size",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="storage_type",
            field=models.CharField(
                blank=True,
                choices=[("SSD", "SSD"), ("HDD", "HDD"), ("Hybrid", "Hybrid")],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="laptop",
            name="thunderbolt_support",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="laptop",
            name="touchscreen",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="laptop",
            name="usb_ports",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="webcam_resolution",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="laptop",
            name="weight",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=5, null=True
            ),
        ),
        migrations.AlterField(
            model_name="laptop",
            name="battery_life",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="laptop",
            name="brand",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="laptop",
            name="graphics_card",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="laptop",
            name="os",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="laptop",
            name="processor",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="laptop",
            name="ram",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="laptop",
            name="screen_size",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=4, null=True
            ),
        ),
    ]
