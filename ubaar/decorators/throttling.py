# your_app/decorators/throttling.py

from functools import wraps
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
