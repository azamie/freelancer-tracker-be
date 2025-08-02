import logging

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response = Response(
                {
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )

            # Set JWT cookies
            response.set_cookie(
                "access_token",
                str(access_token),
                max_age=60 * 60,
                httponly=True,
                secure=False,
                samesite="Lax",
            )
            response.set_cookie(
                "refresh_token",
                str(refresh),
                max_age=7 * 24 * 60 * 60,
                httponly=True,
                secure=False,
                samesite="Lax",
            )

            return response
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                logger.warning("Failed to blacklist refresh token: %s", e)

        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response


class RefreshTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            response = Response(
                {"message": "Token refreshed successfully"},
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                "access_token",
                str(access_token),
                max_age=60 * 60,
                httponly=True,
                secure=False,
                samesite="Lax",
            )

            return response

        except Exception as e:
            logger.warning("Invalid refresh token: %s", e)
            return Response(
                {"error": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
