from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CustomUserSerializer
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    
    def list(self, request, *args, **kwargs):
        print("Queryset:", self.queryset)  # Debug the queryset
        response = super().list(request, *args, **kwargs)
        print("Response Data:", response.data)  # Debug the serialized data
        return response