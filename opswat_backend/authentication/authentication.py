from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that reads the token from cookies
    instead of the Authorization header
    """

    def authenticate(self, request):
        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return super().authenticate(request)

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        return (user, validated_token)
