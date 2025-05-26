from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.db import IntegrityError
from django.views.generic import TemplateView
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from core.custom_api import CustomAPIView
from .serializers import UserRegistrationSerializer, JobSerializer, QuoteSerializer
from .authentication import CustomIsAuthenticated
from .utils import send_activation_email, get_user_from_token, revoke_token, is_token_valid

from jobs.models import Job, Quote
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

User = get_user_model()

class RegisterAppUser(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Register a new user in the application.
        """
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        confirm_password = request.data.get('confirm_password', None)

        if email is None or password is None or confirm_password is None:
            return Response({"data: Missing Data"}, status=status.HTTP_400_BAD_REQUEST)

        data_validation_errors = []

        if password != confirm_password:
            data_validation_errors.append("Passwords do not match.")

        try:
            validator = EmailValidator()
            validator(email)
        except ValidationError as e:
            print(e)
            data_validation_errors.append(e.messages)

        if len(data_validation_errors) > 0:
            return Response({"data": data_validation_errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                is_active=False,
            )
            user.save()
        
        except IntegrityError as e:
            print(e)
            return Response({"data": "User with this email already exists."}, status=status.HTTP_409_CONFLICT)

        success = send_activation_email(user)
        if not success:
            return Response({"data": "Failed to send activation email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"data": "User registered successfully. Please check your email to activate your account."}, status=status.HTTP_201_CREATED)

class ActivateAccount(TemplateView):
    template_name = 'api/account_activation.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        token = kwargs['token']

        if token is None or not is_token_valid(token):
            context['failed_reason'] = "Invalid or expired token."
            return self.render_to_response(context)

        try:
            user = get_user_from_token(token)
            # revoke invite token, makes token single use
            revoke_token(token)

        except User.DoesNotExist:
            context['failed_reason'] = "User not found for the provided token."
            return self.render_to_response(context)
        
        user.is_active = True
        user.save()
        return self.render_to_response(context)
    
    # Generate new tokens for the user
        # refresh = RefreshToken.for_user(user)
        # access_token = str(refresh.access_token)

        # # Add tokens to the context for the response
        # context['access_token'] = access_token
        # context['refresh_token'] = str(refresh)

        # return self.render_to_response(context)

class LoginDataApi(GenericAPIView):
    def get(self, request):
        data = {
            'message': 'You are logged in!'
        }
        return JsonResponse(data, status=status.HTTP_200_OK)

class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # Validate and create the user
        user_serializer = UserRegistrationSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class JobCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = JobSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class QuoteCreateAPIView(CustomAPIView):
    permission_classes = []

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        print('trying csrf dispatch')
        return super().dispatch(*args, **kwargs)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        print(f"Authenticated user: {request.user}")   # Debugging line to check request data
        serializer = QuoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)  # Debugging line to check errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class JobListAPIView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_queryset(self):
        # Optionally filter jobs by the currently authenticated user
        user = self.request.user
        if user.is_authenticated:
            return Job.objects.filter(created_by=user, is_deleted=False)
        return Job.objects.none()
    
class QuoteListAPIView(ListAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def get_queryset(self):
        # Optionally filter quotes by the currently authenticated user
        user = self.request.user
        if user.is_authenticated:
            return Quote.objects.filter(created_by=user, is_deleted=False)
        return Quote.objects.none()
    
class JobDeleteAPIView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            job = Job.objects.get(pk=pk, created_by=request.user, is_deleted=False)
            job.is_deleted = True
            job.deleted_date = now()
            job.save()
            return Response({"message": "Job deleted successfully."}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"error": "Job not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)
        
class QuoteDeleteAPIView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            quote = Quote.objects.get(pk=pk, created_by=request.user, is_deleted=False)
            quote.is_deleted = True
            quote.deleted_date = now()
            quote.save()
            return Response({"message": "Quote deleted successfully."}, status=status.HTTP_200_OK)
        except Quote.DoesNotExist:
            return Response({"error": "Quote not found or already deleted."}, status=status.HTTP_404_NOT_FOUND)
        
class JobUpdateAPIView(UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def put(self, request, pk, *args, **kwargs):
        try:
            job = Job.objects.get(pk=pk)
            if job.is_deleted:
                return Response({"error": "Cannot update a deleted job."}, status=status.HTTP_400_BAD_REQUEST)
        except Job.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuoteUpdateAPIView(UpdateAPIView):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

    def put(self, request, *args, **kwargs):
        try:
            quote = Quote.objects.get(pk=kwargs['pk'], created_by=request.user)
            if quote.is_deleted:
                raise ValidationError({"error": "No Quote matches the given query."})
        except Quote.DoesNotExist:
            raise ValidationError({"error": "Quote not found."})
        
        serializer = QuoteSerializer(quote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AgreeQuoteAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):
        try:
            quote = Quote.objects.get(pk=pk, created_by=request.user)

            # Check if the quote is in the correct state
            if quote.status != Quote.Status.SENT:
                raise ValueError("This quote has already been accepted or is not in a valid state to be accepted.")
            
            job = quote.agree_and_create_job()
            return Response({
                "message": "Quote accepted and job created successfully.",
                "job_id": job.id,
                "job_status": job.status
            }, status=status.HTTP_200_OK)
        
        except Quote.DoesNotExist:
            return Response({"error": "Quote not found or not in a valid state to be accepted."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)