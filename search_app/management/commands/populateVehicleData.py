from django.core.management.base import BaseCommand
from faker import Faker
from faker_vehicle import VehicleProvider
import random
from search_app.models import Car

class Command(BaseCommand):
    help = 'Populate database with fake car rental data'

    def handle(self, *args, **options):
        fake = Faker()
        fake.add_provider(VehicleProvider)
        colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'black', 'white', 'brown', 'magenta', 'beige']
        for _ in range(100):  # Generate 100 fake car entries
            car = Car(
                make=fake.vehicle_make(),
                model=fake.vehicle_model(),
                year=fake.vehicle_year(),
                rental_price=fake.random_number(digits=3),
                color=random.choice(colors),
            )
            car.save()
            
        self.stdout.write(self.style.SUCCESS('Fake car rental data generated successfully'))
