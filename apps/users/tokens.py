"""
    Tokens file.
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        token['email'] = user.email
        token['first_name'] = user.first_name
        return token

class CustomRefreshToken(RefreshToken):
    """
    Custom Refresh Token Class.
    """
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["email"] = user.email
        token.lifetime = timedelta(seconds=3600)  
        return token

def get_tokens_for_user(user):
    refresh = CustomRefreshToken.for_user(user)
    access = AccessToken.for_user(user)
    access.set_exp(lifetime=timedelta(seconds=3600))  # Set custom expiration

    # Add custom claims
    refresh['email'] = user.email
    access['is_staff'] = user.is_staff
    access['email'] = user.email
    access['first_name'] = user.first_name

    return {
        "refresh": str(refresh),
        "access": str(access),
    }

def token_decoder(token):
    try:
        token_obj = AccessToken(token)
        return token_obj.payload['user_id']
    except TokenError as e:
        raise Exception(f"Invalid token: {str(e)}")
