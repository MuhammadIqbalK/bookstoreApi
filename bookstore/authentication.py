from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Memanggil JWT Authentication standar untuk memvalidasi token
        user_and_token = super().authenticate(request)

        if not user_and_token:
            return None

        user, token = user_and_token

        # Mendapatkan klaim `iat` (issued at) dari token
        iat_timestamp = token.get('iat')
        if iat_timestamp is None:
            raise AuthenticationFailed('Token missing `iat` claim.')

        # Mendapatkan `logout_at` dari user (misalnya, dari field database)
        logout_at = user.logout_at  # Pastikan ini sudah ada di model User

        if logout_at:
            logout_at_timestamp = logout_at.timestamp()
            # Validasi: Jika token dibuat sebelum logout, maka token tidak valid
            if iat_timestamp < logout_at_timestamp:
                raise AuthenticationFailed('Token has been invalidated due to logout.')

        return user, token
