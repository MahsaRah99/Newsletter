from rest_framework import serializers
from .models import User
import re as regex


def clean_phone(value):
    pattern = r"^(\+98|0)9\d{9}$"

    if regex.match(pattern, value):
        return
    else:
        return serializers.ValidationError("enter a avalid phone number")


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        exclude = ("is_active", "is_active")
        extra_kwargs = {
            "password": {"write_only": True},
            "phone_number": {"validators": (clean_phone,)},
        }

    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if value == "admin":
            raise serializers.ValidationError("username cant be `admin`")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("passwords must match")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("is_active",)
