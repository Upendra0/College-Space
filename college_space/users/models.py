''' User model '''

import pyotp
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .managers import MyUserManager
from resources.models import Note, Book, QuestionPaper, WebTutorial, VideoTutorial


def validate_image_size(file: models.FileField, limit_mb = 1):
    ''' Validate a file's size does not exceed limit size'''

    file_size = file.file.size
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of file is { limit_mb } MB")

class User(AbstractBaseUser, PermissionsMixin):
    
    ''' user object '''

    email = models.EmailField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    department = models.ForeignKey(to='resources.department', db_column='dept_name', on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/',
                                    validators=[validate_image_size],
                                    null = True,
                                    blank = True,
                                    )
    date_joined = models.DateField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    #32 char secret key needed for otp creation.                                
    secret_key = models.CharField(max_length=35, default=pyotp.random_base32)
    interval = 900
    
    #Primary key fields.
    USERNAME_FIELD = 'email'
    #Fields required to create superuser.
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    class Meta:
        db_table = 'user'

    def __str__(self) -> str:
        ''' str representation for user object.'''

        return self.email

    def send_otp(self):
        ''' Send otp to user's email address.'''

        otp= pyotp.TOTP(self.secret_key, interval=self.interval).now()
        subject = "College Space - OTP for account Activation"
        msg = f"Hii {self.email}  your otp for email verification is {otp}"
        send_mail(subject=subject, message=msg, from_email=None, recipient_list=[self.email], fail_silently=True)

    def verify_otp(self, otp):
        ''' Verify if otp match for user.'''

        totp= pyotp.TOTP(self.secret_key, interval=self.interval)
        return totp.verify(otp)

    def get_department(self, request):
        '''Return department of user from user's profile or session variable, none if not avialable.'''

        if self.department:
            return self.department
        return request.session.get('dept_name', None)

    def get_semester(self, request):
        '''Return semester of user from user's profile or session variable, none if not avialable.'''

        if self.semester:
            return self.semester
        return request.session.get('semester', None)

    def total_non_verified_items(self):
        ''' Return total items added by user in database which is not verified.'''

        total = 0
        models = [Note, QuestionPaper, Book, VideoTutorial, WebTutorial]
        for model in models:
            total+=model.total_not_verified(self)
        return total

    def can_contribute(self):
        '''Return bool wheather user is egligble to contribute or not.'''

        contribution_limit = 5
        return self.total_non_verified_items()<=contribution_limit