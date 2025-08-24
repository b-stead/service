from django.test import TestCase
from django.contrib.auth import get_user_model
from customers.models import Customer
from jobs.models import Job, Quote

User = get_user_model()


class JobModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )

        # Create a customer
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            created_by=self.user,
            updated_by=self.user,
        )

    def test_create_standalone_job(self):
        """Test creating a standalone job."""
        job = Job.objects.create(
            title="Fix Plumbing",
            description="Fix the leaking sink in the kitchen.",
            customer=self.customer,
            created_by=self.user,
            start_date="2023-10-01",
            recurrence="none",
        )
        self.assertEqual(job.title, "Fix Plumbing")
        self.assertFalse(job.is_recurring())

    def test_create_recurring_job(self):
        """Test creating a recurring job."""
        job = Job.objects.create(
            title="Weekly Lawn Mowing",
            description="Mow the lawn every week.",
            customer=self.customer,
            created_by=self.user,
            start_date="2023-10-01",
            recurrence="weekly",
            recurrence_interval=1,
        )
        self.assertEqual(job.title, "Weekly Lawn Mowing")
        self.assertTrue(job.is_recurring())
        self.assertEqual(job.recurrence, "weekly")
        self.assertEqual(job.recurrence_interval, 1)


class QuoteModelTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email="testuser@example.com", password="password123"
        )

        # Create a customer
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            created_by=self.user,
            updated_by=self.user,
        )

        # Create a job
        self.job = Job.objects.create(
            title="Fix Plumbing",
            description="Fix the leaking sink in the kitchen.",
            customer=self.customer,
            created_by=self.user,
            start_date="2023-10-01",
        )

    def test_create_quote(self):
        """Test creating a quote."""
        quote = Quote.objects.create(
            title="Plumbing Work",
            description="Fix the leaking sink and replace the faucet.",
            customer=self.customer,
            job=self.job,
            created_by=self.user,
            total_price=250.00,
        )
        self.assertEqual(quote.title, "Plumbing Work")
        self.assertEqual(quote.customer, self.customer)
        self.assertEqual(quote.job, self.job)
        self.assertEqual(quote.total_price, 250.00)
        self.assertEqual(quote.status, Quote.Status.DRAFT)

    def test_update_quote_status(self):
        """Test updating the status of a quote."""
        quote = Quote.objects.create(
            title="Plumbing Work",
            customer=self.customer,
            created_by=self.user,
            total_price=250.00,
        )
        quote.status = Quote.Status.ACCEPTED
        quote.save()
        self.assertEqual(quote.status, Quote.Status.ACCEPTED)
