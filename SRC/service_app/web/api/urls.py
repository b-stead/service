from django.contrib import admin
from django.urls import path, include
from .views import CustomUserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]