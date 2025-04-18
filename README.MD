# 🟦 Ubaar task

## User Flow — تجربه کاربری

۱. **کاربر شماره موبایل خود را وارد می‌کند.**  
۲. **کد تأیید (OTP) به شماره ارسال می‌شود.**  
۳. **کاربر پس از دریافت OTP، آن را در برنامه وارد می‌کند.**  
۴. **در صورت نیاز، رمز عبور نیز وارد می‌شود.**  
۵. **در صورت ورود موفق، توکن یا پیام تأیید بازمی‌گردد.**

---

## OTP Rate Limiting
- بعد از هر ارسال OTP، باید **۳ دقیقه** صبر شود.

## block after 3 unsuccessfull attemps
- بیش از **۳ تلاش ناموفق** (ورود اشتباه رمز یا OTP) در مدت **۱ ساعت** باعث **بلاک شدن** موقت کاربر می‌شود.

---

## API Endpoints

### 1. درخواست کد ورود (registered or not)

`POST /api/auth/request-login/`

####  Request Body:

```json
{
  "phone_number": "09123456789"
}
```

#### output
```json
{
    "registered": true or false
}
```
## if registered = false
### 2. درخواست کد یک بار مصرف (OTP)
`POST /api/auth/request-otp/`

####  Request Body:

```json
{
  "phone_number": "09123456789"
}
```
#### output
```json
{
    "detail": "کد ارسال شد (کد: ******)"
}
```

## اگر قبل از سه دقیقه درخواست بزند
```json
{
    "detail": "لطفاً ۳ دقیقه صبر کنید و سپس دوباره تلاش کنید."
}
```

### صحت سنجی کد یک بار مصرف
`POST /api/auth/verify-otp/`

####  Request Body:

```json
{
    "phone_number": "09369109944", 
    "code": "841839"
}
```

#### output

```json
{
    "detail": "ورود موفق",
    "new_user": true
}
```

#### اگر بیشتر از سه بار اشتباه بزند
```json
{
    "detail": "به دلیل تلاش‌های ناموفق، دسترسی شما به مدت ۱ ساعت محدود شده است."
}
```

### اضافه کردن نام و نام خانوادگی
`POST /api/auth/set-profile/`

####  Request Body:

```json
{
    "phone_number": "09369109944", 
    "first_name": "علی", 
    "last_name": "سمیع زاده"
}
```

#### output
```json
{
    "detail": "اطلاعات با موفقیت ذخیره شد"
}
```

### اضافه کردن پسورد
`POST /api/auth/set-password/`

####  Request Body:

```json
{
    "phone_number": "09369109944", 
    "password": "12345678"
}
```

#### output
```json
{
    "message": "رمز عبور با موفقیت تنظیم شد."
}
```

## if registered = true

### لاگین با پسورد
`POST /api/auth/login-password/`

####  Request Body:

```json
{
    "phone_number": "09369109944", 
    "password": "1235678"
}
```
#### output

```json
{
    "detail": "ورود موفق"
}
```

#### اگر بیشتر از سه بار اشتباه بزند
```json
{
    "detail": "به دلیل تلاش‌های ناموفق، دسترسی شما به مدت ۱ ساعت محدود شده است."
}
```
