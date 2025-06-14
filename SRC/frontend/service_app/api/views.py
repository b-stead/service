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
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.custom_api import CustomAPIView
from .serializers import UserRegistrationSerializer, JobSerializer, QuoteSerializer
from .authentication import CustomIsAuthenticated
from .utils import send_activation_email, get_user_from_token, revoke_token, CustomTokenObtainPairSerializer, CustomJWTAuthentication

from jobs.models import Job, Quote
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
import requests
import jwt
from django.conf import settings
from .auth import authenticate_user, create_access_token, TokenAuthentication

User = get_user_model()

class RegisterAppUser(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        confirm_password = request.data.get('confirm_password', None)
        if not email or not password or not confirm_password:
            return Response({"error": "Email, password, and confirm_password are required."}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Validate email format
            validator = EmailValidator()
            validator(email)
        except ValidationError as e:
            data_validation_errors = {"email": str(e)}
            if len(data_validation_errors) > 0:
                return Response(data_validation_errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Create user
            user = User.objects.create_user(email=email, password=password)
            user.is_active = False  # Set user as inactive until email is verified
            user.save()
            # Send activation email
            send_activation_email(user)
            return Response({"message": "User registered successfully. Please check your email to activate your account."}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccount(TemplateView):
    template_name = 'account_activation.html'    

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        token = request.GET.get('token', None)
        if not token:
            context['error'] = "Activation token is required."
            return self.render_to_response(context)
        try:
            user = get_user_from_token(token)
            revoke_token(token)  # Revoke the token after use

            user.is_active = True
            user.save()
            context['message'] = "Your account has been activated successfully."
        except User.DoesNotExist:
            context['error'] = "User not found."
            return self.render_to_response(context)
        
        user.is_active = True
        user.save()
        context['message'] = "Your account has been activated successfully."
        return self.render_to_response(context)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print(response.data)  # Debugging: Print the token payload
        return response

class TestAPIView(GenericAPIView):
    # return a JSON response with a message
    #permission_classes = [AllowAny]
    def get(self, request):

        data = {
            "message": "This is a test response from the TestAPIView."
        }
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
    
class LoginAPIView(APIView):
    """Exchange a valid Google ID token for an access token."""
    def post(self, request):
        id_token = request.data.get('id_token')
        if not id_token:
            return Response({"detail": "ID token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sub = authenticate_user(id_token=id_token)
        except jwt.exceptions.InvalidTokenError as err:
            return Response({"detail": f"Invalid ID token: {err}"}, status=status.HTTP_400_BAD_REQUEST)

        if not sub:
            return Response({"detail": "Invalid ID token."}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = create_access_token(data={'sub': sub})
        return JsonResponse({
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.TOKEN_LIFETIME_SECONDS
        }, status=status.HTTP_200_OK)
    
class JobCreateAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # print(f"Request data: {request.data}")  # Debugging: Log request data

        serializer = JobSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Save the job with the authenticated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # print(f"Serializer errors: {serializer.errors}")  # Debugging: Log serializer errors
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
    
class JobListAPIView(APIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "Authorization header is missing or invalid"}, status=401)

        token = auth_header.split(' ')[1]
        try:
            decoded_token = AccessToken(token)
            print(f"Decoded token payload: {decoded_token.payload}")  # Debugging: Print the token payload

            sub = decoded_token.get('sub')
            if not sub:
                return Response({"error": "Token does not contain a subject"}, status=400)

            # Fetch jobs for the user with the given sub
            user = request.user
            jobs = Job.objects.filter(created_by=user, is_deleted=False)
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            print(f"Error decoding token: {e}")
            return Response({"error": "Failed to decode token"}, status=400)
    
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