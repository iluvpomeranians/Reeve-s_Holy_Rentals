
import os
import glob
from django.core.files import File
from django.core.management.base import BaseCommand
from search_app.models import Car

class Command(BaseCommand):
    help = 'Populate database with fake car rental data'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--directory', type=str, help='Directory containing car images', default='/Users/josephaladas/Desktop/soen341-HolyKeanuReeves/src/Reeves_Holy_Rentals/media/car_images')

    def handle(self, *args, **options):
        image_directory = options['directory']
        image_path_pattern = os.path.join(image_directory, 'Car_*.jpg')  # assuming images are jpg format
        
        for car_image_path in glob.glob(image_path_pattern):
            car_id = int(os.path.basename(car_image_path).split('_')[1].split('.')[0])  # Extracting car ID from image filename
            try:
                car = Car.objects.get(id=car_id)
                with open(car_image_path, 'rb') as f:
                    car.image.save(os.path.basename(car_image_path), File(f))
                    self.stdout.write(self.style.SUCCESS(f'Image linked for Car ID: {car_id}'))
            except Car.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Car with ID: {car_id} does not exist in the database'))


            