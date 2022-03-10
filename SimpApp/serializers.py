from rest_framework import serializers
from SimpApp.models import MyUser
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=58, min_length=10, write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                "Username should only contain alphanumeric characters")
        return attrs

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = MyUser
        fields = ["token"]


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=10)
    password = serializers.CharField(
        max_length=72, min_length=10, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=10, read_only=True)
    tokens = serializers.CharField(
        max_length=68, min_length=6, read_only=True)

    class Meta:

        model = MyUser
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, Try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled")

        if not user.is_verified:
            raise AuthenticationFailed("Account is not verified")

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super.validate(attrs)