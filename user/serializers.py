from rest_framework import serializers
from django.contrib.auth import password_validation as validators

from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password', 'email', 'first_name', 'last_name', 'role', 'phone']

    def validate_password(self, data):
            validators.validate_password(password=data, user=CustomUser)
            return data

    def create(self, data):
        user = CustomUser(
            **data
        )
        user.set_password(data['password'])
        user.save()
        return user
    
class AuthRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)