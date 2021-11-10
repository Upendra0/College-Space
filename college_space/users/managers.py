''' Contain the user model's manager.'''

from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):

    '''' user model's manager.'''

    def create_user(self, email: str, password: str, first_name: str, last_name: str, is_active: bool, is_staff: bool, is_superuser: bool):
        
        ''' Creates, save user into database and return user.'''

        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, first_name: str, last_name: str):

        ''' Create the superuser (user with is_superuser=True) and return user.'''

        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        return user
