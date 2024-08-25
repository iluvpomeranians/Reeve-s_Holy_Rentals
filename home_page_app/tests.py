from django.test import TestCase, Client
from home_page_app.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'firstName': 'John',
            'lastName': 'Doe',
            'driverLicense': '1234567890',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'membership': True,
            'paymentinfo': {'card_number': '1234', 'expiry_date': '12/25'},
            'dateofbirth': '1990-01-01',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }
        self.user = get_user_model().objects.create(**self.user_data)

    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.firstName, self.user_data['firstName'])
        self.assertEqual(self.user.lastName, self.user_data['lastName'])
        self.assertEqual(self.user.driverLicense, self.user_data['driverLicense'])
        self.assertEqual(self.user.address, self.user_data['address'])
        self.assertEqual(self.user.city, self.user_data['city'])
        self.assertEqual(self.user.state, self.user_data['state'])
        self.assertEqual(self.user.membership, self.user_data['membership'])
        self.assertEqual(self.user.paymentinfo, self.user_data['paymentinfo'])
        self.assertEqual(str(self.user.dateofbirth), self.user_data['dateofbirth'])
        self.assertEqual(self.user.is_active, self.user_data['is_active'])
        self.assertEqual(self.user.is_staff, self.user_data['is_staff'])
        self.assertEqual(self.user.is_superuser, self.user_data['is_superuser'])

    def test_string_representation(self):
        """Test string representation of user"""
        expected_string = f"{self.user.email} {self.user.firstName} {self.user.lastName}"
        self.assertEqual(str(self.user), expected_string)

    def test_has_perm(self):
        """Test user permissions"""
        # Here, assuming has_perm always returns True
        self.assertTrue(self.user.has_perm('any_permission'))

    def test_has_module_perms(self):
        """Test module permissions"""
        # Here, assuming has_module_perms always returns True
        self.assertTrue(self.user.has_module_perms('any_app_label'))
