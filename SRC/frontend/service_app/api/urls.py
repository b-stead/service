from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterAppUser.as_view(), name='register'),
    path('activate_account/<str:token>/', views.ActivateAccount.as_view(), name='activate_account'),
    path('logged_in_data/', views.LoginDataApi.as_view(), name='logged_in_data'),

    path('auth/token/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),


    path('signup/', views.UserRegistrationAPIView.as_view(), name='api_signup'),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    

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
