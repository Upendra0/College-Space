import os
import pyotp
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from .managers import MyUserManager
from django.core.mail import send_mail

def validate_image_size(file):
    file_size = file.file.size
    limit_mb = 1
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is { limit_mb } MB")


def profile_directory_path(instance, filename):
    f_name, extension = os.path.splitext(filename)
    user = f"{instance.first_name}({instance.email}){extension}"
    return f'profile_pics/{user}'

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.ForeignKey(to='resources.department', db_column='dept_name', on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], null=True, blank=True)
    profile_pic = models.ImageField(default='profile_pics/default.jpeg',
                                    upload_to=profile_directory_path,
                                    validators=[validate_image_size]
                                    )
    secret_key = models.CharField(max_length=35, default=pyotp.random_base32)
    date_joined = models.DateField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = MyUserManager()
    interval = 900

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'user'

    def __str__(self) -> str:
        return self.email

    def send_otp(self):
        otp= pyotp.TOTP(self.secret_key, interval=self.interval).now()
        subject = "College Space - OTP for account Activation"
        msg = f"Hii {self.email}  your otp for email verification is {otp}"
        send_mail(subject=subject, message=msg, from_email=None, recipient_list=[self.email], fail_silently=True)

    def verify_otp(self, otp):
        totp= pyotp.TOTP(self.secret_key, interval=self.interval)
        return totp.verify(otp)

    