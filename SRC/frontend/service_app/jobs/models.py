from django.db import models
from django.conf import settings
from customers.models import Customer

class Job(models.Model):
    class RecurrenceType(models.TextChoices):
        NONE = "none", "No Recurrence"
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        FORTNIGHTLY = "fortnightly", "Fortnightly"
        MONTHLY = "monthly", "Monthly"
        BIMONTHLY = "bimonthly", "Bimonthly"
        QUARTERLY = "quarterly", "Quarterly"
        SEMIANNUALLY = "semiannually", "Semiannually"
        ANNUALLY = "annually", "Annually"
        CUSTOM = "custom", "Custom"
        WEEKDAY = "weekday", "Weekday"
        WEEKEND = "weekend", "Weekend"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="jobs"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="jobs_created",
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="jobs_updated",
        null=True,
        blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    recurrence = models.CharField(
        max_length=12,
        choices=RecurrenceType.choices,
        default=RecurrenceType.NONE
    )
    recurrence_interval = models.PositiveIntegerField(
        default=1,
        help_text="Interval for recurrence (e.g., every 2 weeks)."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.customer})"

    def is_recurring(self):
        return self.recurrence != self.RecurrenceType.NONE


class Quote(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="quotes"
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        related_name="quotes",
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="quotes_created",
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="quotes_updated",
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quote: {self.title} for {self.customer}"