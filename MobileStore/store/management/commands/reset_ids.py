from django.core.management.base import BaseCommand
from django.db import models, connection
from django.apps import apps

class Command(BaseCommand):
    def handle(self, *args, **options):
        for model in apps.get_models():
            if issubclass(model, models.Model):
                with connection.cursor() as cursor:
                    cursor.execute(f"ALTER SEQUENCE {model._meta.db_table}_id_seq RESTART WITH 1;")
                self.stdout.write(f"Reset ID for {model.__name__}")