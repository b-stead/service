from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', views.UserRegistrationAPIView.as_view(), name='api_signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

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
