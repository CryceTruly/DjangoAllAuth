from rest_framework import authentication
from rest_framework import exceptions
from .models import User
import jwt


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        header = request.META.get('HTTP_AUTHORIZATION', None)
        if header is None:
            raise exceptions.AuthenticationFailed(
                "Authentication credentials were not provided")

        token = header.split(" ")[1]
        return self.get_user_from_token(token, request)

    def get_user_from_token(self, token, request):

        try:
            user = jwt.decode(token, 'secret')
            new_user = User.objects.filter(username=user['username']).first()

            return (new_user, token)
        except Exception as identifier:
            raise exceptions.AuthenticationFailed("Token is not valid")
