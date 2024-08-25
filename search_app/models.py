"""
models.py: Contains database models for the search app.
"""
from django.db import models
from django.db.models import JSONField


class Car(models.Model):
    """
    Car represents a vehicle that can be rented.
    """
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=60)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    location = models.CharField(max_length=60)

    def __str__(self):
        return (
            f"{self.year} {self.make} {self.model} "
            f"{self.color} {self.rental_price} {self.location}"
        )
class Reservation(models.Model):
    """
    Reservation represents a booking of a vehicle by a customer.
    """
    car_id = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    driver_license = models.CharField(max_length=100)
    check_in = models.DateField(null=True, blank=True)
    check_out = models.DateField(null=True, blank=True)
    check_in_data = JSONField(null=True, blank=True)
    check_out_data = JSONField(null=True, blank=True)
    rental_agreement_signed = models.BooleanField(null=True, blank=True)
    rental_agreement_signed_date = models.DateField(null=True, blank=True)
    insurance_purchased = models.BooleanField(null=True, blank=True)
    deposit_paid = models.BooleanField(null=True, blank=True)
    fees_paid = models.BooleanField(null=True, blank=True)
    email_sent = models.BooleanField(null=True, blank=True)


    def __str__(self):
        return f"Reservation for {self.customer_name} ({self.customer_email})"
