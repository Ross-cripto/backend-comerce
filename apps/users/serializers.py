
"""
Serializers for the user API View
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import VerificationCode
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password", "confirm_password"]

    def validate(self, data):
        if not data.get("old_password") or not data.get("new_password") or not data.get("confirm_password"):
            raise serializers.ValidationError({"error": "Todos los campos son requeridos"})

        if not self.instance.check_password(data.get("old_password")):
            raise serializers.ValidationError({"error": "Contraseña antigua incorrecta"})

        if data.get("new_password") != data.get("confirm_password"):
            raise serializers.ValidationError({"error": "Las nuevas contraseñas no coinciden"})

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "role"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.is_active = False
        user.save()
        return user


class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCode
        fields = ['code']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ["id","email", "password", "first_name", "last_name", "role"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
