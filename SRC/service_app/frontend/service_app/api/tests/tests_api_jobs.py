from django.test import TestCase
from django.contrib.auth import get_user_model
from customers.models import Customer
from jobs.models import Job, Quote
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.timezone import now
from django.conf import settings
import jwt
from datetime import datetime, timedelta

User = get_user_model()

class JobCreateAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword123")
        self.customer = Customer.objects.create(first_name="Test Customer")
        self.client.login(email="testuser@example.com", password="securepassword123")
        self.job_create_url = "/api/jobs/create/"

    def test_create_job(self):
        data = {
            "title": "Test Job",
            "description": "This is a test job.",
            "start_date": "2023-10-01",
            "customer": self.customer.id,
            "status": "pending"
        }
        response = self.client.post(self.job_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(Job.objects.first().title, "Test Job")

class QuoteCreateAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword123", sub="somerandomstring")
        self.customer = Customer.objects.create(first_name="Test Customer")
        self.quote_create_url = "/api/quotes/create/"

        # Encode the sub token as a JWT
        self.sub_token = jwt.encode(
            {
                "sub": "somerandomstring",  # The unique identifier for the user
                "exp": datetime.utcnow() + timedelta(minutes=5)  # Token expires in 5 minutes
            },
            settings.SECRET_KEY,  # Use the same secret key as your application
            algorithm="HS256"  # Use the same algorithm as your application
        )

    def test_create_quote(self):
        data = {
            "title": "Test Quote",
            "description": "This is a test quote.",
            "customer": self.customer.id,
            "status": "draft",
            "total_price": "100.00"
        }
        # Include the Authorization header with the encoded JWT token
        headers = {"HTTP_AUTHORIZATION": f"Bearer {self.sub_token}"}
        response = self.client.post(self.quote_create_url, data, format="json", **headers)
        print("Response data:", getattr(response, "data", response.content))  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(Quote.objects.first().title, "Test Quote")


class JobListAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword123")
        self.client.login(email="testuser@example.com", password="securepassword123")
        self.customer = Customer.objects.create(first_name="Test Customer")
        self.job1 = Job.objects.create(title="Job 1", customer=self.customer, created_by=self.user, start_date="2023-10-01")
        self.job2 = Job.objects.create(title="Job 2", customer=self.customer, created_by=self.user, start_date="2023-10-02", is_deleted=True)
        self.job_list_url = "/api/jobs/"

    def test_list_jobs(self):
        response = self.client.get(self.job_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Job 1")

class QuoteListAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword123")
        self.client.login(email="testuser@example.com", password="securepassword123")
        self.customer = Customer.objects.create(first_name="Test Customer")
        self.quote1 = Quote.objects.create(title="Quote 1", customer=self.customer, created_by=self.user, total_price="100.00")
        self.quote2 = Quote.objects.create(title="Quote 2", customer=self.customer, created_by=self.user, total_price="100.00", is_deleted=True)
        self.quote_list_url = "/api/quotes/"

    def test_list_quotes(self):
        response = self.client.get(self.quote_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Quote 1")

class JobUpdateAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword123")
        self.client.login(email="testuser@example.com", password="securepassword123")
        self.customer = Customer.objects.create(first_name="Test Customer")
        self.job = Job.objects.create(title="Job 1", customer=self.customer, created_by=self.user, start_date="2023-10-01")
        self.job2 = Job.objects.create(title="Job 2", customer=self.customer, created_by=self.user, start_date="2023-10-01", is_deleted=True)
        self.job2.deleted_date = now()
        self.job2.save()
        self.job_update_url = f"/api/jobs/{self.job.id}/update/"

    def test_update_job(self):
        data = {
            "title": "Updated Job Title",
            "description": "Updated description.",
            "start_date": "2023-10-05",
            "customer": self.customer.id,
        }
        response = self.client.put(self.job_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, "Updated Job Title")
        self.assertEqual(self.job.description, "Updated description.")
        self.assertEqual(str(self.job.start_date), "2023-10-05")

    def test_update_deleted_job(self):
        self.job.is_deleted = True
        self.job.deleted_date = now()
        self.job.save()
        data = {
            "title": "Job 1"
        }
        response = self.client.put(self.job_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Cannot update a deleted job.")


class QuoteUpdateAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword123")
        self.client.login(email="testuser@example.com", password="securepassword123")
        self.customer = Customer.objects.create(first_name="Test Customer")
        self.quote = Quote.objects.create(title="Quote 1", customer=self.customer, created_by=self.user, total_price="100.00")
        self.quote_update_url = f"/api/quotes/{self.quote.id}/update/"

    def test_update_quote(self):
        data = {
            "title": "Updated Quote Title",
            "description": "Updated description.",
            "total_price": "150.00"
        }
        response = self.client.put(self.quote_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quote.refresh_from_db()
        self.assertEqual(self.quote.title, "Updated Quote Title")
        self.assertEqual(self.quote.description, "Updated description.")
        self.assertEqual(str(self.quote.total_price), "150.00")

    def test_update_deleted_quote(self):
        self.quote.is_deleted = True
        self.quote.deleted_date = now()
        self.quote.save()
        data = {
            "title": "Updated Quote Title"
        }
        response = self.client.put(self.quote_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "No Quote matches the given query.")

class JobDeleteAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword123")
        self.client.login(email="testuser@example.com", password="securepassword123")
        self.customer = Customer.objects.create(first_name="Test Customer")
        self.job = Job.objects.create(title="Job 1", customer=self.customer, created_by=self.user, start_date="2023-10-01")
        self.job_delete_url = f"/api/jobs/{self.job.id}/delete/"

    def test_delete_job(self):
        response = self.client.delete(self.job_delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.job.refresh_from_db()
        self.assertTrue(self.job.is_deleted)
        self.assertIsNotNone(self.job.deleted_date)

    def test_delete_nonexistent_job(self):
        response = self.client.delete("/api/jobs/999/delete/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Job not found or already deleted.")


class QuoteDeleteAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword123")
        self.client.login(email="testuser@example.com", password="securepassword123")
        self.customer = Customer.objects.create(first_name="Test Customer")
        self.quote = Quote.objects.create(title="Quote 1", customer=self.customer, created_by=self.user, total_price="100.00")
        self.quote_delete_url = f"/api/quotes/{self.quote.id}/delete/"

    def test_delete_quote(self):
        response = self.client.delete(self.quote_delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quote.refresh_from_db()
        self.assertTrue(self.quote.is_deleted)
        self.assertIsNotNone(self.quote.deleted_date)

    def test_delete_nonexistent_quote(self):
        response = self.client.delete("/api/quotes/999/delete/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Quote not found or already deleted.")

class AgreeQuoteAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="securepassword123")
        self.client.login(email="testuser@example.com", password="securepassword123")
        self.customer = Customer.objects.create(first_name="Test Customer")
        self.quote = Quote.objects.create(
            title="Test Quote",
            description="This is a test quote.",
            total_price="100.00",
            customer=self.customer,
            created_by=self.user,
            status=Quote.Status.SENT
        )
        self.agree_quote_url = f"/api/quotes/{self.quote.id}/agree/"

    def test_agree_quote_creates_job(self):
        response = self.client.post(self.agree_quote_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quote.refresh_from_db()
        self.assertEqual(self.quote.status, Quote.Status.ACCEPTED)
        self.assertIsNotNone(self.quote.job)
        self.assertEqual(self.quote.job.status, Job.Status.PENDING)

    def test_agree_already_accepted_quote(self):
        self.quote.status = Quote.Status.ACCEPTED
        self.quote.save()
        response = self.client.post(self.agree_quote_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "This quote has already been accepted or is not in a valid state to be accepted.")

    def test_agree_nonexistent_quote(self):
        response = self.client.post("/api/quotes/999/agree/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Quote not found or not in a valid state to be accepted.")