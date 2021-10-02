from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
import os
from django.contrib.auth.password_validation import validate_password
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

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    department_type_choices = (
        ('cse', 'Computer Science & engineering'),
        ('ce', 'Civil engineering'),
        ('ee', 'Electrical engineering'),
        ('ece', 'Electronics and communication engineering'),
        )

    email = models.EmailField( verbose_name="email address", max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255, choices=department_type_choices)
    semester = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    profile_pic = models.ImageField(default='profile_pics/default.jpeg',
                                    upload_to=profile_directory_path,
                                    validators=[validate_image_size]
                                    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department', 'semester']

    def __str__(self) -> str:
        return self.email