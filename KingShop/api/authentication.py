from datetime import timezone, timedelta

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if token.created < timezone.now() - timedelta(minutes=1):
            token.delete()
            user = token.user
            token = Token.objects.create(user=user)

        return (token.user, token)