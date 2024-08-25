from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from home_page_app.models import User
from .models import Reservation, Car

class CheckinTestCase(TestCase):
    def setUp(self):
        # Create test user and reservation
        self.user = User.objects.create_user( 'test@example.com', 'testpassword')
        self.reservation = Reservation.objects.create(
            # user=self.user,
            car_id='1',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            # Initialize other necessary fields
        )

    def test_checkin_view(self):
        self.client.login(username='test@example.com', password='testpassword')
        url = reverse('checkin', args=[self.reservation.id])
        response = self.client.post(url, {
            'engine': 'true',
            'transmission': 'true',
            # Add other fields as needed
        })

        self.assertEqual(response.status_code, 200)
        self.reservation.refresh_from_db()
        self.assertTrue(self.reservation.check_in_data)  # Assumes check_in_data is updated by the view

class CheckoutTestCase(TestCase):
    def setUp(self):
        # Create test user and reservation
        self.user = User.objects.create_user( 'test@example.com', 'testpassword')
        self.reservation = Reservation.objects.create(
            # user=self.user,
            car_id='1',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timezone.timedelta(days=1),
            # Initialize other necessary fields
        )

    def test_checkout_view(self):
        self.client.login(username='test@example.com', password='testpassword')
        url = reverse('checkout', args=[self.reservation.id])
        response = self.client.post(url, {
            'engine': 'true',
            'transmission': 'true',
            # Add other fields as needed
        })

        self.assertEqual(response.status_code, 200)
        self.reservation.refresh_from_db()
        # self.assertTrue(self.reservation.check_out_data)  # Assumes check_out_data is updated by the view

class ReservationTestCase(TestCase):
    def setUp(self):
        # Create a user with the custom user model
        user = User.objects.create_user(
            email="john@example.com",
            password="testpassword123",  # This password will be hashed automatically
            firstName="John",
            lastName="Doe",
            driverLicense="123456789",
            address="123 Main St",
            city="Anytown",
            state="Anystate",
            membership=True,
            paymentinfo={"credit_card_number": "1234567890123456", "expiration_date": "01/23", "cvv": "123"},
            dateofbirth=date(1990, 1, 1)
        )

        # Create a car instance
        car = Car.objects.create(make="Toyota", model="Camry", year=2022, rental_price=100.00, color="Red")

        # Create a reservation instance, assuming it references the Car and User models
        Reservation.objects.create(
            car=car,
            start_date=date(2024, 3, 1),
            end_date=date(2024, 3, 10),
            customer=user,  # Assuming the 'customer' field now correctly references the custom User model
            driver_license="12345"
        )

class CarTestCase(TestCase):
    def setUp(self):
        Car.objects.create(make="Toyota", model="Camry", year=2022, rental_price=100.00, color="Yellow")
        Car.objects.create(make="Honda", model="Civic", year=2023, rental_price=120.00, color="DarkGreen")

    def test_car_str_representation(self):
        car1 = Car.objects.get(make="Toyota", model="Camry", year=2022, rental_price=100.00, color="Yellow")
        car2 = Car.objects.get(make="Honda", model="Civic", year=2023, rental_price=120.00, color="DarkGreen")
        self.assertEqual(str(car1), "2022 Toyota Camry Yellow 100.00 ")
        self.assertEqual(str(car2), "2023 Honda Civic DarkGreen 120.00 ")

