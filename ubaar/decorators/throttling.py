from functools import wraps
from rest_framework.response import Response
from django.utils import timezone
from ..models import LoginAttempt, RegisterAttempt , OTPCode

from rest_framework.response import Response
from django.utils import timezone
from ..models import LoginAttempt, RegisterAttempt

def block_check(login=True):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[0]
            phone = request.data.get('phone_number')

            model = LoginAttempt if login else RegisterAttempt
            one_hour_ago = timezone.now() - timezone.timedelta(hours=1)

            filters = {
                'ip_address': ip,
                'timestamp__gte': one_hour_ago,
                'successful': False,
            }
            if phone:
                filters['phone_number'] = phone

            failed_attempts = model.objects.filter(**filters).count()

            if failed_attempts >= 3:
                return Response(
                    {"detail": "به دلیل تلاش‌های ناموفق، دسترسی شما به مدت ۱ ساعت محدود شده است."},
                    status=403
                )
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator



def otp_rate_limit():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[0]
            phone = request.data.get('phone_number')
            if not phone:
                return Response({'detail': 'شماره موبایل ارسال نشده است.'}, status=400)

            three_minutes_ago = timezone.now() - timezone.timedelta(minutes=3)

            recent_otp = OTPCode.objects.filter(
                phone_number=phone,
                created_at__gte=three_minutes_ago
            ).order_by('-created_at').first()

            if recent_otp:
                return Response({'detail': 'لطفاً ۳ دقیقه صبر کنید و سپس دوباره تلاش کنید.'}, status=429)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
