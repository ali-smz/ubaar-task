from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import Count
from django.utils.decorators import method_decorator
from .decorators.throttling import block_check , otp_rate_limit
from .models import User, OTPCode, LoginAttempt, RegisterAttempt
from .serializers import (
    PhoneNumberSerializer, PasswordLoginSerializer,
    OTPRequestSerializer, OTPVerifySerializer, ProfileSerializer
)
import random


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')

class RequestLoginView(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            user_exists = User.objects.filter(phone_number=phone).exists()
            return Response({'registered': user_exists}, status=200)
        return Response(serializer.errors, status=400)


class PasswordLoginView(APIView):
    @block_check(login=True)
    def post(self, request):
        serializer = PasswordLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            user = authenticate(request, phone_number=phone, password=password)

            ip = get_client_ip(request)
            LoginAttempt.objects.create(ip_address=ip, phone_number=phone, successful=bool(user))

            if user:
                return Response({'detail': 'ورود موفق'}, status=200)
            else:
                return Response({'detail': 'شماره یا رمز اشتباه است.'}, status=401)
        return Response(serializer.errors, status=400)


@method_decorator(otp_rate_limit(), name='post')
class OTPRequestView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            code = f"{random.randint(100000, 999999)}"
            OTPCode.objects.create(phone_number=phone, code=code)
            return Response({'detail': f'کد ارسال شد (کد: {code})'}, status=200)
        return Response(serializer.errors, status=400)



class OTPVerifyView(APIView):
    @block_check(login=False)
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            ip = get_client_ip(request)
            phone = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']

            otp = OTPCode.objects.filter(phone_number=phone, code=code, is_used=False).last()
            if otp and not otp.is_expired():
                otp.is_used = True
                otp.save()

                user, created = User.objects.get_or_create(phone_number=phone)
                if created:
                    user.is_active = True
                    user.save()

                RegisterAttempt.objects.create(ip_address=ip, phone_number=phone, successful=True)
                return Response({'detail': 'ورود موفق', 'new_user': created}, status=200)
            else:
                RegisterAttempt.objects.create(ip_address=ip, phone_number=phone, successful=False)
                return Response({'detail': 'کد نامعتبر یا منقضی شده است'}, status=400)
        return Response(serializer.errors, status=400)


class ProfileUpdateView(APIView):
    def post(self, request):
        user = User.objects.filter(phone_number=request.data.get('phone_number')).first()
        if not user:
            return Response({'detail': 'کاربر پیدا نشد'}, status=404)

        serializer = ProfileSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'اطلاعات با موفقیت ذخیره شد'}, status=200)
        return Response(serializer.errors, status=400)
    

class SetPasswordView(APIView):
    def post(self, request):
        phone = request.data.get("phone_number")
        password = request.data.get("password")

        if not phone or not password:
            return Response({"error": "شماره موبایل و رمز عبور الزامی هستند."}, status=400)

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return Response({"error": "کاربری با این شماره پیدا نشد."}, status=404)

        user.set_password(password)
        user.save()
        return Response({"message": "رمز عبور با موفقیت تنظیم شد."}, status=200)
