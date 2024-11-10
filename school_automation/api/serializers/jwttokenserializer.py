from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .usermodel import UserModelSerializer
from ..models import UserModel

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        user_data = UserModelSerializer(user).data
        data['user'] = user_data
        return data

    @classmethod
    def get_token(cls, phone_number):
        token = super().get_token(phone_number)
        return token

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['refresh'] = str(refresh)        
        return data



