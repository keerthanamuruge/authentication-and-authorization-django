from django.contrib import auth
from psycopg2 import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, attrs):
        password = attrs.get('password', '')
        confrim_password = attrs.get('password_confirm', '')

        if not password.isalnum():
            raise serializers.ValidationError('password must be alpha numeric')
        if password and password != confrim_password:
            raise serializers.ValidationError('Passwords do not match')
        attrs.pop('password_confirm')
        return attrs

    def create(self, validated_data):
        try:
            User.objects.create_user(**validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError("User Already exists.")

    def create_tl(self, validated_data):
        try:
            User.objects.create_tl(**validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError("User Already exists.")

class LoginSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            "access": user.tokens()['access_token'],
            "refresh": user.tokens()['refresh_token']
        }

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'tokens')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credential')

        if not user.is_active:
            raise AuthenticationFailed('Account is disabled, please contact admin')

        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            }
