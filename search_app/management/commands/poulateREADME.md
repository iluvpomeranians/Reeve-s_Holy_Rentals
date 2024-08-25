# Action

Populating fake data

## Table of Contents

- [Settings.py](#Settings.py)
- [Create Class](#Models.py)
- [Migrate](#makemigration)
- [Populate](#populatescript)

## Settings.py

Check project-level Settings.py and make sure the app you are going to edit is in INSTALLED_APPS: 

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home_page_app',
    'search_app',
    '<add_new_app_here_1>,
    '<add_new_app_here_2>,
    '<add_new_app_here_3>,
]
```

## Models.py

Create a class in models.py of the app you are working in: 

```py 
from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} {self.color} {self.rental_price}"
```
## Migrate

After creating new classes in models.py, we migrate these new models to our datbase by runnning:

```shell
    python manage.py makemigrations
    python manage.py migrate
```

## Populate.py

- Create a populate.py script

```py
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
```

- Now we run our populate script: 

```sh
    python manage.py name_of_script_here
```


