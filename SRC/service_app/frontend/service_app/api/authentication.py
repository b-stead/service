from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import SessionAuthentication


class CustomIsAuthenticated(BasePermission):
    """
    Custom permission class that checks if the user is authenticated
    using the custom authentication logic.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Custom authentication class that disables CSRF checks.
    """

    def enforce_csrf(self, request):
        # Skip CSRF validation
        return


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Try to authenticate using the access token
        try:
            return super().authenticate(request)
        except AuthenticationFailed as e:
            # If the access token is invalid or expired, try to refresh it
            refresh_token = request.COOKIES.get("refresh") or request.headers.get(
                "Authorization-Refresh"
            )
            print("trying refresh")
            if not refresh_token:
                raise AuthenticationFailed(
                    "Authentication credentials were not provided."
                )

            try:
                # Attempt to refresh the access token
                new_access_token = RefreshToken(refresh_token).access_token
                # Set the new access token in the response headers or cookies
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {str(new_access_token)}"
                return super().authenticate(request)
            except TokenError:
                raise AuthenticationFailed("Invalid or expired refresh token.")
