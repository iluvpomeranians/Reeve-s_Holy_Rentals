from django.db import migrations, models
import csv
from django.conf import settings
import os

def import_car_data(apps, schema_editor):
    Car = apps.get_model('search_app', 'Car')

    csv_file_path = os.path.join(settings.BASE_DIR, 'car_out.csv')

    with open(csv_file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Car.objects.create(
                make=row['make'],
                model=row['model'],
                year=int(row['year']),
                rental_price=row['rental_price'],
                color=row['color'],
                # Assuming `image` is handled by a path or left blank
                # If your CSV includes an image path, you can include it as below. Otherwise, omit or set to None.
                image=row.get('image', None),
                location=row['location']
            )

class Migration(migrations.Migration):

    dependencies = [
        ('search_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_car_data),
    ]
