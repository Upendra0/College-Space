from django.core import validators
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import os

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, department,semester):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            department = department,
            semester = semester,
        )

        user.set_password(password)
        user.save()
        return user 

    def create_superuser(self, email, password, first_name, last_name, department,semester):
        user = self.create_user(
            email=email, 
            password=password,
            first_name=first_name, 
            last_name=last_name,
            department=department,
            semester = semester,
        )
        user.is_admin = True
        user.save()
        return user 


class User(AbstractBaseUser):
    department_type_choices = (
    ('cse', 'Computer Science & engineering'),
    ('ce', 'Civil engineering'),
    ('ee', 'Electrical engineering'),
    ('ece', 'Electronics and communication engineering'),
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    department = models.CharField( max_length=255, choices=department_type_choices)
    semester = models.SmallIntegerField(blank=False, null=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department', 'semester']

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self) -> str:
        return self.email




def ids_directory_path(instance, filename):
    f_name, extension = os.path.splitext(filename)
    user = instance.user.first_name + '( '+ instance.user.email +' )' + extension
    return 'college_ids/' + user

class Contributor(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    college_id = models.ImageField(
        upload_to= ids_directory_path,
        validators=[validators.validate_image_file_extension],
        )

    def __str__(self) -> str:
        return self.user.first_name + '( ' + self.user.email +' )'
