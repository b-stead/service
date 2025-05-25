from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from core.custom_api import CustomAPIView
from .serializers import UserRegistrationSerializer, JobSerializer, QuoteSerializer
from .authentication import CustomIsAuthenticated

from jobs.models import Job, Quote
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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