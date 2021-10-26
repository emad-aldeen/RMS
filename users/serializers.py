from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class UsersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['username', 'created_at']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=4, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '') 

        
        try:
            user = User.objects.get(email=email, password=password)
        except:
            try:
                user = auth.authenticate(email=email, password=password)
            except:
                raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Action disabled, contact Admin')
        
        return{
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }
