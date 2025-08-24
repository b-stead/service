from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Company
from customers.models import Customer
from customers.models import Address

User = get_user_model()


class CustomerModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )

        # Create a company
        self.company = Company.objects.create(name="Test Company", owner=self.user)

        # Create an address
        self.address = Address.objects.create(
            street="123 Main St",
            city="Test City",
            state="Test State",
            postal_code="12345",
            country="Test Country",
        )

        # Create a customer
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            address=self.address,
            company=self.company,
            created_by=self.user,
            updated_by=self.user,
        )

    def test_customer_creation(self):
        """Test that a customer is created successfully."""
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertEqual(self.customer.email, "john.doe@example.com")
        self.assertEqual(self.customer.phone, "1234567890")
        self.assertEqual(self.customer.address, self.address)
        self.assertEqual(self.customer.company, self.company)
        self.assertEqual(self.customer.created_by, self.user)
        self.assertEqual(self.customer.updated_by, self.user)

    def test_customer_update(self):
        """Test updating a customer's details."""
        self.customer.first_name = "Jane"
        self.customer.last_name = "Smith"
        self.customer.save()

        self.assertEqual(self.customer.first_name, "Jane")
        self.assertEqual(self.customer.last_name, "Smith")

    def test_customer_deletion(self):
        """Test deleting a customer."""
        self.customer.delete()
        self.assertEqual(Customer.objects.count(), 0)

    def test_customer_with_no_address(self):
        """Test creating a customer without an address."""
        customer_without_address = Customer.objects.create(
            first_name="Alice",
            last_name="Brown",
            email="alice.brown@example.com",
            phone="9876543210",
            company=self.company,
            created_by=self.user,
            updated_by=self.user,
        )
        self.assertIsNone(customer_without_address.address)
        self.assertEqual(customer_without_address.company, self.company)

    def test_customer_with_no_company(self):
        """Test creating a customer without a company."""
        customer_without_company = Customer.objects.create(
            first_name="Bob",
            last_name="Green",
            email="bob.green@example.com",
            phone="5555555555",
            address=self.address,
            created_by=self.user,
            updated_by=self.user,
        )
        self.assertIsNone(customer_without_company.company)
        self.assertEqual(customer_without_company.address, self.address)
