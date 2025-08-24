from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import Company

User = get_user_model()


class UserRegistrationAPITestCase(APITestCase):
    def setUp(self):
        # Set up any initial data if needed
        self.signup_url = "/api/signup/"

    def test_user_registration_without_company(self):
        """Test registering a user without a company"""
        data = {
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": "securepassword123",
            "is_company": False,
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Company.objects.count(), 0)

    def test_user_registration_with_company(self):
        """Test registering a user with a company"""
        data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "securepassword123",
            "is_company": True,
            "company_name": "Test Company",
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Company.objects.count(), 1)
        company = Company.objects.first()
        self.assertEqual(
            company.name, "test company"
        )  # Ensure company name is normalized
        self.assertEqual(company.owner.email, "testuser2@example.com")

    def test_user_registration_with_missing_company_name(self):
        """Test registering a user as a company without providing a company name"""
        data = {
            "username": "testuser3",
            "email": "testuser3@example.com",
            "password": "securepassword123",
            "is_company": True,
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("company_name", response.data)

    def test_user_registration_with_duplicate_company(self):
        """Test registering a user with a duplicate company"""
        # Create an initial user and company
        user = User.objects.create_user(
            email="existinguser@example.com",
            password="securepassword123",
            first_name="Existing",
            last_name="User",
        )
        Company.objects.create(name="duplicate company", owner=user)

        # Attempt to register a new user with the same company name
        data = {
            "username": "testuser4",
            "email": "testuser4@example.com",
            "password": "securepassword123",
            "is_company": True,
            "company_name": "Duplicate Company",
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("company_name", response.data)
        self.assertEqual(
            response.data["company_name"], "A company with this name already exists."
        )

    def test_user_registration_with_existing_email(self):
        """Test registering a user with an email that already exists"""
        User.objects.create_user(
            email="duplicateemail@example.com",
            password="securepassword123",
            first_name="Existing",
            last_name="User",
        )
        data = {
            "username": "testuser5",
            "email": "duplicateemail@example.com",
            "password": "securepassword123",
            "is_company": False,
        }
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
