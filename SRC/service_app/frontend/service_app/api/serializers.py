from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from users.models import Company
from django.db import transaction
from jobs.models import Job, Quote

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    is_company = serializers.BooleanField(default=False, write_only=True)
    company_name = serializers.CharField(
        max_length=255, required=False, write_only=True
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "is_company",
            "company_name",
        ]

    def validate(self, data):
        # If the user is signing up as a company, ensure company_name is provided
        if data.get("is_company") and not data.get("company_name"):
            raise serializers.ValidationError(
                {"company_name": "This field is required for company registration."}
            )
        # Validate the password
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        is_company = validated_data.pop("is_company", False)
        company_name = validated_data.pop("company_name", None)

        # Create the user
        with transaction.atomic():
            # Create the user
            user = User.objects.create_user(
                email=validated_data["email"],
                password=validated_data["password"],
                first_name=validated_data.get("first_name", ""),
                last_name=validated_data.get("last_name", ""),
            )

            # If the user is signing up as a company, create the company
            if is_company:
                company_name = company_name.lower()  # Normalize company name

                # Check if the user already owns a company
                if Company.objects.filter(owner=user).exists():
                    raise serializers.ValidationError(
                        {"company": "This user already owns a company."}
                    )

                try:
                    Company.objects.create(name=company_name, owner=user)
                except Exception as e:
                    raise serializers.ValidationError(
                        {"company_name": "A company with this name already exists."}
                    )

            return user


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "customer",
            "created_by",
            "status",
            "created_at",
            "updated_at",
            "is_deleted",
            "deleted_date",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def create(self, validated_data):
        # Automatically set the `created_by` field to the currently authenticated user
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = [
            "id",
            "title",
            "description",
            "customer",
            "job",
            "created_by",
            "status",
            "total_price",
            "created_at",
            "updated_at",
            "is_deleted",
            "deleted_date",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def create(self, validated_data):
        print(f" data is {self.context['request']}")
        # Automatically set the `created_by` field to the currently authenticated user
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
