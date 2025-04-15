from django.contrib import admin
from .models import UserManager,OTPCode,User,LoginAttempt,RegisterAttempt
# Register your models here.
admin.site.register(OTPCode)
admin.site.register(LoginAttempt)
admin.site.register(RegisterAttempt)