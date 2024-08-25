from django.core.management.base import BaseCommand
from faker import Faker
from home_page_app.models import User
import uuid

class Command(BaseCommand):
    help = 'Populate database with fake user data'

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(200):  
            # Use the create_user method to ensure passwords are hashed
            plaintext_password = fake.password(length=12)
            # print(f"Generated password: {plaintext_password}")
            user = User.objects.create_user(
                email=fake.email(),
                password=plaintext_password,  # This password will be hashed automatically
                firstName=fake.first_name(),
                lastName=fake.last_name(),
                driverLicense=str(fake.random_number(digits=9)),  
                address=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                membership=fake.boolean(chance_of_getting_true=50),
                paymentinfo={ 
                    "credit_card_number": fake.credit_card_number(),
                    "expiration_date": fake.credit_card_expire(),
                    "cvv": fake.credit_card_security_code(),
                },
                dateofbirth=fake.date_of_birth(minimum_age=18, maximum_age=90)  
            )
            # No need to call user.save() as create_user already saves the user instance

        self.stdout.write(self.style.SUCCESS('Fake user data generated successfully'))

        ### For login testing: ###
        ##########################
        #gonzalezscott@example.net
        #!kGux*vFTI2L
