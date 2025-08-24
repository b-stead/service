from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.views import View
import requests

User = get_user_model()


class OAuthLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        provider = request.data.get("provider")  # 'google' or 'microsoft'
        token = request.data.get("token")  # OAuth token from the app

        if provider not in ["google", "microsoft"]:
            return Response(
                {"detail": "Invalid provider."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Verify the token with the provider
        user_info = self.verify_token(provider, token)
        if not user_info:
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create the user in your database
        user, created = User.objects.get_or_create(
            email=user_info["email"],
            defaults={
                "first_name": user_info.get("first_name", ""),
                "last_name": user_info.get("last_name", ""),
                "is_active": True,  # Automatically activate users from OAuth
            },
        )

        # Issue JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK,
        )

    def verify_token(self, provider, token):
        """
        Verify the OAuth token with the provider and return user info.
        """
        if provider == "google":
            url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"

        elif provider == "microsoft":
            url = f"https://graph.microsoft.com/v1.0/me"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None

        data = response.json()
        if provider == "google":
            return {
                "email": data.get("email"),
                "first_name": data.get("given_name"),
                "last_name": data.get("family_name"),
            }


class OAuthLoginView(View):
    def get(self, request, *args, **kwargs):
        # Render the OAuth login page
        return render(request, "oauth/login.html", {})

    def post(self, request, *args, **kwargs):
        # Handle OAuth login submission
        return OAuthLoginAPIView.as_view()(request, *args, **kwargs)
