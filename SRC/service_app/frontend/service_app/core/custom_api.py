from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings

User = get_user_model()


class CustomAPIView(APIView):
    """
    Custom APIView that handles authorization using a 'sub' token.
    """

    def get_sub_from_token(self, request):
        """
        Extract and validate the 'sub' token from the Authorization header.
        """
        print("Extracting token from Authorization header...")
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            print("Authorization header is missing or invalid.")
            return None, Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split(" ")[1]  # Extract the token
        try:
            # Decode the token
            print("Decoding token...")
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            sub = payload.get("sub")
            print(f"Token decoded successfully. 'sub' value: {sub}")
            if not sub:
                print("Token is invalid: 'sub' not found.")
                return None, Response(
                    {"detail": "Invalid token: 'sub' not found."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Check token expiration
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(
                timezone.utc
            ):
                print("Token has expired. Generating a new token...")
                # Token is expired, create a new expiration time
                new_exp = datetime.now() + timedelta(minutes=1)
                payload["exp"] = int(new_exp.timestamp())
                new_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
                print("New token generated successfully.")
                return sub, {
                    "new_token": new_token
                }  # Return the new token for the client

            print("Token is valid.")
            return sub, None
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            return None, Response(
                {"detail": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError:
            print("Token is invalid.")
            return None, Response(
                {"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED
            )

    def authenticate_user(self, sub):
        """
        Authenticate the user based on the 'sub' value.
        """
        try:
            user = User.objects.get(sub=sub)
            return user
        except User.DoesNotExist:
            return None

    # def check_permissions(self, request):
    #     """
    #     Override the default permission checks to ensure the user is authenticated
    #     using custom logic.
    #     """
    #     if not request.user or not request.user.is_authenticated:
    #         # If the user is not authenticated, raise an error
    #         self.permission_denied(
    #             request,
    #             message="Authentication credentials were not provided.",
    #             code="not_authenticated",
    #         )

    def dispatch(self, request, *args, **kwargs):
        """
        Override the dispatch method to handle authorization.
        """
        print("Dispatch method called. Checking token...")
        sub, response_or_token = self.get_sub_from_token(request)
        if not sub:
            print("Token is invalid or missing. Returning 401 response.")
            self.headers = {}
            return self.finalize_response(request, response_or_token, *args, **kwargs)

        # Authenticate the user
        print(f"Token is valid. Authenticating user with sub: {sub}")
        user = self.authenticate_user(sub)
        if not user:
            print(f"User with sub '{sub}' not found. Returning 401 response.")
            self.headers = {}
            response = Response(
                {"detail": "Invalid user."}, status=status.HTTP_401_UNAUTHORIZED
            )
            return self.finalize_response(request, response, *args, **kwargs)

        # Attach the user to the request
        print(
            f"User authenticated successfully. Attaching user '{user}' to the request."
        )
        request.user = user

        # If a new token was generated, include it in the response headers
        if isinstance(response_or_token, dict) and "new_token" in response_or_token:
            print("New token generated. Attaching it to the request.")
            request.new_token = response_or_token["new_token"]

        print("Dispatch method completed. Proceeding to the view.")
        return super().dispatch(request, *args, **kwargs)
