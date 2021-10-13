import os
import pyotp
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from .managers import MyUserManager

def validate_image_size(file):
    file_size = file.file.size
    limit_mb = 1
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)


def profile_directory_path(instance, filename):
    f_name, extension = os.path.splitext(filename)
    user = instance.first_name + '( ' + instance.email + ' )' + extension
    return 'profile_pics/' + user

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
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()
    interval = 600

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'user'

    def __str__(self) -> str:
        return self.email

    def generate_otp(self):
        return pyotp.TOTP(self.secret_key, interval=self.interval)

    def verify_otp(self):
        return pyotp.TOTP(self.secret_key, interval=self.interval).verify()

    