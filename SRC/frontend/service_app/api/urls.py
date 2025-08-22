from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),

    path('register/', views.RegisterAppUser.as_view(), name='register'),
    path('activate/<str:token>/', views.ActivateAccount.as_view(), name='activate'),
    
    path('auth/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # obtain jwt with email and password
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh expired token

    path('test/', views.TestAPIView.as_view(), name='test'),
    # Jobs
    path('jobs/create/', views.JobCreateAPIView.as_view(), name='job-create'),
    path('quotes/create/', views.QuoteCreateAPIView.as_view(), name='quote-create'),
    path('jobs/', views.JobListAPIView.as_view(), name='job-list'),
    path('quotes/', views.QuoteListAPIView.as_view(), name='quote-list'),
    path('jobs/<int:pk>/delete/', views.JobDeleteAPIView.as_view(), name='job-delete'),
    path('quotes/<int:pk>/delete/', views.QuoteDeleteAPIView.as_view(), name='quote-delete'),
    path('jobs/<int:pk>/update/', views.JobUpdateAPIView.as_view(), name='job-update'),
    path('quotes/<int:pk>/update/', views.QuoteUpdateAPIView.as_view(), name='quote-update'),
    path('quotes/<int:pk>/agree/', views.AgreeQuoteAPIView.as_view(), name='quote-agree'),
]
