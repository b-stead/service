from django.test import TestCase
from .models import CustomUser, Company

# FILE: SRC/serv_app/frontend/serv_app/serv_app/test_settings.py


class CustomUserModelTests(TestCase):
    def test_create_regular_user(self):
        """Test creating a regular user."""
        user = CustomUser.objects.create_user(
            email="user@example.com",
            password="password123",
            role=CustomUser.UserRole.STAFF,
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(user.role, CustomUser.UserRole.STAFF)
        self.assertIsNone(user.company)

    def test_create_company_owner(self):
        """Test creating a company owner and associating them with a company."""
        owner = CustomUser.objects.create_user(
            email="owner@example.com",
            password="password123",
            role=CustomUser.UserRole.COMPANY_OWNER,
        )
        company = Company.objects.create(name="Test Company", owner=owner)
        self.assertEqual(company.name, "Test Company")
        self.assertEqual(company.owner, owner)
        self.assertEqual(owner.role, CustomUser.UserRole.COMPANY_OWNER)
        self.assertEqual(owner.owned_company, company)

    def test_assign_staff_to_company(self):
        """Test assigning staff users to a company."""
        owner = CustomUser.objects.create_user(
            email="owner@example.com",
            password="password123",
            role=CustomUser.UserRole.COMPANY_OWNER,
        )
        company = Company.objects.create(name="Test Company", owner=owner)
        staff_user = CustomUser.objects.create_user(
            email="staff@example.com",
            password="password123",
            role=CustomUser.UserRole.STAFF,
            company=company,
        )
        self.assertEqual(staff_user.company, company)
        self.assertIn(staff_user, company.staff.all())

    def test_invalid_superuser_creation(self):
        """Test validation for creating a superuser with incorrect flags."""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email="superuser@example.com",
                password="password123",
                is_staff=False,
            )
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(
                email="superuser@example.com",
                password="password123",
                is_superuser=False,
            )
