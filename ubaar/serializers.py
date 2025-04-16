from rest_framework import serializers
from .models import User

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) <= 10:
            raise serializers.ValidationError("شماره موبایل نامعتبر است.")
        return value

class PasswordLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField()

class OTPRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) <= 10:
            raise serializers.ValidationError("شماره موبایل نامعتبر است.")
        return value

class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.CharField(max_length=6)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

